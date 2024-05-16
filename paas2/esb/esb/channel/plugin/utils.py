import glob
import json
import os
import shutil
import tarfile
import tempfile

from django.db.models import Q

from common.django_utils import JsonResponse
from components.generic.templates.cmsi.toolkit.tools import get_base64_icon
from conf.default import BASE_DIR
from esb.bkcore.models import ESBChannel, ComponentSystem
from esb.management.commands.sync_system_and_channel_data import Command
from components.generic.templates.cmsi.toolkit import configs as msg_type_config
from components.esb_conf import config
from esb.component.base import *


class Esb_channel_plugin(object):
    def __init__(self, request):
        self.request = request
        self.config_data = None
        self.name = None
        self.IAM_channel_type = request.POST.get('code', '')
        self.esb_conf_config = config
        self.cmp_name = None
        self.channel_path = None
        self.is_active = True
        self.channel_method = 'POST'
        self.channel_cmp_sys_id = ComponentSystem.objects.get(name=msg_type_config.SYSTEM_NAME).id
        self.channel_type = 1
        self.update = False

    # 检查配置参数
    def pre_check(self):
        if not self.cmp_name or not self.channel_path:
            missing_params = []
            if not self.cmp_name:
                missing_params.append("component_name")
            if not self.channel_path:
                missing_params.append("path")

            return JsonResponse({"success": False,
                                 "message": f"Config JSON file does not contain {' and '.join(missing_params)}"})

        existing_item = next((item for item in msg_type_config.msg_type
                              if item.get('type') == self.IAM_channel_type), None)
        if existing_item:
            # 检查是否存在不同的path和cmp_name
            if (existing_item.get('path') != self.channel_path and
                    existing_item.get('cmp_name') != self.cmp_name):
                return JsonResponse({"success": False,
                                     "message": f"Cannot modify existing type: {self.IAM_channel_type} with different path and cmp_name together"})

    def update_mapping(self):
        item_data = {
            "name": self.name,
            "type": self.IAM_channel_type,
            "cmp_name": self.cmp_name,
            "label": self.IAM_channel_type,
            "label_en": self.IAM_channel_type,
            "active_icon": get_base64_icon("icons_v2/default_active.ico"),
            "unactive_icon": get_base64_icon("icons_v2/default_unactive.ico"),
            "is_active": self.is_active,
            "path": self.channel_path,
            "method": self.channel_method,
            "is_builtin": False,
        }

        channel = ESBChannel.objects.get(Q(path=self.channel_path) | Q(component_name=self.cmp_name))
        if channel:
            # 判断是否需要删除目录
            extra_info = json.loads(channel.extra_info)
            if extra_info.get('type') != self.IAM_channel_type:
                old_plugin_dir = os.path.join(BASE_DIR, 'components', 'generic', 'templates', 'cmsi', 'plugins',
                                              str(extra_info.get('type')))
                if os.path.exists(old_plugin_dir):
                    shutil.rmtree(old_plugin_dir)
            extra_info.update(item_data)
            # 将更新后的列表转换回字符串并保存回 channel.extra_info
            channel.extra_info = json.dumps(extra_info)
            channel.save()  # 保存更新后的 channel 对象到数据库

        else:
            return JsonResponse({"success": False, "message": "Channel object does not exist"})

        # 删除mapping信息

    def delete_mapping(self):
        # 检查要删除的类型是否存在于 msg_type_map 中
        if self.IAM_channel_type in msg_type_config.msg_type_map:
            # 删除映射
            del msg_type_config.msg_type_map[self.IAM_channel_type]

        # 检查要删除的类型是否存在于 msg_type 中
        for item in msg_type_config.msg_type:
            if item.get('type') == self.IAM_channel_type:
                # 删除对应的消息类型
                msg_type_config.msg_type.remove(item)
                break  # 找到后跳出循环

    # 创建通道并更新mapping
    def create_esb_plugin_channel(self):
        # Update config_data keys if necessary
        self.config_data.setdefault('extra_info',
                                    {"is_confapi": True, "label_en": f"{self.cmp_name}", "suggest_method": "POST"})

        default_update_fields = ["name", "component_codename", "component_name", "method", "is_hidden"]
        force_update_fields = ["component_system_id", "type", "timeout_time"]
        self.config_data.update({
            "component_codename": f"generic.cmsi.{self.cmp_name}",
            "path": self.channel_path,
            "method": self.channel_method,
            "component_system_id": self.channel_cmp_sys_id,
            "type": self.channel_type,
            "component_name": self.cmp_name,
            "name": self.config_data.get("name", "")
        })

        command = Command()
        try:
            esb_channel = ESBChannel.objects.get(Q(path=self.channel_path) | Q(component_name=self.cmp_name))
            command.force = None
            esb_channel.is_active = self.is_active
            esb_channel.path = self.channel_path
            command.update_channel_by_config(esb_channel, self.config_data, default_update_fields, force_update_fields)
        except ESBChannel.DoesNotExist:
            command.create_channel_by_config(self.config_data, default_update_fields, force_update_fields)

        # 数据库操作成功才更新mapping
        self.update_mapping()

        refresh_components_manager()

    # 处理上传的插件包
    def handle_uploaded_file(self):
        plugin_dir = os.path.join(BASE_DIR, 'components', 'generic', 'templates', 'cmsi', 'plugins',
                                  str(self.request.POST.get('code', '')))

        # 不存在则创建，存在则删除目录下所有文件
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)
        elif os.path.exists(plugin_dir):
            for filename in os.listdir(plugin_dir):
                file_path = os.path.join(plugin_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in self.request.FILES['file'].chunks():
                temp_file.write(chunk)

        if not tarfile.is_tarfile(temp_file.name):
            os.remove(temp_file.name)
            return JsonResponse({"success": False, "message": "Uploaded file is not a valid tar archive"})

        with tarfile.open(temp_file.name, 'r') as tar:
            tar.extractall(path=plugin_dir)

        os.remove(temp_file.name)

        # 读取解压后的 JSON 文件
        channel_config_path = os.path.join(plugin_dir, 'channel_config.json')
        if not os.path.exists(channel_config_path):
            # 如果文件不存在，返回相应的错误信息
            return JsonResponse({"success": False, "message": "channel_config.json file not found"})
        else:
            # 读取 JSON 文件并处理其中的数据
            with open(channel_config_path, 'r') as channel_config_file:
                channel_config_data = json.load(channel_config_file)
                # 更新对象属性值
                self.update_properties_from_json(channel_config_data)

                # 检查指定目录下是否存在任何 .py 文件
                py_files = glob.glob(os.path.join(plugin_dir, "*.py"))
                if not py_files:
                    # 如果指定目录下不存在任何 .py 文件，返回相应的错误信息
                    return JsonResponse({"success": False, "message": "No .py files found"})

                # 预检查
                return self.pre_check()

    # 从 JSON 数据中更新对象属性
    def update_properties_from_json(self, config_data):
        self.name = config_data.get('name', '')
        self.config_data = config_data
        self.cmp_name = config_data.get('component_name', '')
        self.channel_path = f"/cmsi{config_data['path']}" if 'path' in config_data else None  # path 需以/开头
        self.is_active = config_data.get('is_active', True)

    def get_cmsi_plugin_channel(self):
        return ESBChannel.objects.filter_channels(system_ids=self.channel_cmp_sys_id, is_hidden=None, is_active=None)


class Esb_edit_channel(Esb_channel_plugin):
    def __init__(self, request):
        super().__init__(request)
        self.body_data = json.loads(request.body.decode('utf-8'))
        self.IAM_channel_type = self.body_data.get('code', '')
        self.config_data = self.body_data.get('config', '')
        self.is_active = self.config_data.get('is_active') if 'is_active' in self.config_data else True

    # 编辑消息通道参数
    def edit_channel(self):
        existing_item = next((item for item in msg_type_config.msg_type
                              if (item.get('type') == self.IAM_channel_type)), None)
        if not existing_item:
            return JsonResponse({"success": False,
                                 "message": f"Can not find channel in map: {self.IAM_channel_type} "
                                            f"Existing channels config in map: {msg_type_config.msg_type_map}"})

        self.channel_path = existing_item.get('path')

        command = Command()
        try:
            esb_channel = ESBChannel.objects.get(Q(path=self.channel_path))
            command.force = None
            esb_channel.is_active = self.is_active
            self.cmp_name = esb_channel.component_name

            # 只更新存在于 comp_conf 数据中的键
            comp_conf_db = json.loads(esb_channel.comp_conf)

            updated_comp_conf = []
            for item in self.config_data.get("comp_conf_to_db", []):
                key = item[0]
                value = item[1]
                for entry in comp_conf_db:
                    if key in entry:
                        updated_comp_conf.append([key, value])

            # Update config_data keys if necessary
            self.config_data.setdefault('extra_info',
                                        {"is_confapi": True, "label_en": f"{self.cmp_name}", "suggest_method": "POST"})

            self.config_data.update({
                "path": self.channel_path,
                "comp_conf_to_db": updated_comp_conf,
                "method": self.channel_method
            })

            command.update_channel_by_config(esb_channel, self.config_data, [], [])
        except ESBChannel.DoesNotExist:
            return JsonResponse({"success": False,
                                 "message": f"Can not find channel in database: {self.IAM_channel_type}"})

        # 数据库操作成功才更新mapping
        self.update_mapping()

        refresh_components_manager()

    def delete_channel(self):
        existing_item = next((item for item in msg_type_config.msg_type
                              if (item.get('type') == self.IAM_channel_type)), None)

        if not existing_item:
            return JsonResponse({"success": False,
                                 "message": f"Can not find channel in mapping: {self.IAM_channel_type}"})
        else:
            self.channel_path = existing_item.get('path')

            try:
                esb_channel = ESBChannel.objects.get(Q(path=self.channel_path))
                esb_channel.delete()
            except ESBChannel.DoesNotExist:
                return JsonResponse({"success": False,
                                     "message": f"Can not find channel in database: {self.IAM_channel_type}"})

            self.delete_mapping()

            # 删除插件包目录
            plugin_dir = os.path.join(BASE_DIR, 'components', 'generic', 'templates', 'cmsi', 'plugins',
                                      str(existing_item.get('type')))
            if os.path.exists(plugin_dir):
                shutil.rmtree(plugin_dir)

            refresh_components_manager()
