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
        self.im_channel_type = request.POST.get('code', '')
        self.esb_conf_config = config
        self.cmp_name = None
        self.channel_path = None
        self.is_active = False
        self.channel_method = 'POST'
        self.channel_cmp_sys_id = ComponentSystem.objects.get(name=msg_type_config.SYSTEM_NAME).id
        self.channel_type = 1
        self.update = False
        self.channels_in_database = ESBChannel.objects.filter_channels(system_ids=[self.channel_cmp_sys_id],
                                                                       is_hidden=None, is_active=None)

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

        for channel in self.channels_in_database:
            if channel.extra_info:
                if self.im_channel_type == json.loads(channel.extra_info).get("type", ""):
                    # 检查是否存在不同的path和cmp_name
                    if (channel.path != self.channel_path and
                            channel.component_name != self.cmp_name):
                        return JsonResponse({"success": False,
                                             "message": f"Cannot modify existing type: {self.im_channel_type} with different path and cmp_name together"})

    def update_mapping(self):
        item_data = {
            "name": self.name,
            "type": self.im_channel_type,
            "cmp_name": self.cmp_name,
            "label": self.name,
            "label_en": self.im_channel_type,
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
            if extra_info.get('type') != self.im_channel_type:
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

    # 创建通道并更新mapping
    def create_esb_plugin_channel(self):
        # Update config_data keys if necessary
        self.config_data.setdefault('extra_info', {
            "is_confapi": True,
            "label_en": f"{self.cmp_name}",
            "suggest_method": self.channel_method
        })

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
            # 尝试获取匹配的ESBChannel记录
            esb_channel = ESBChannel.objects.get(Q(path=self.channel_path) | Q(component_name=self.cmp_name))
            # 删除已存在的记录
            esb_channel.delete()
        except ESBChannel.DoesNotExist:
            pass

        # 创建一个新的ESBChannel记录
        command.create_channel_by_config(self.config_data, default_update_fields, force_update_fields)

        # 获取新创建的ESBChannel记录并设置新的属性
        esb_channel = ESBChannel.objects.get(Q(path=self.channel_path) | Q(component_name=self.cmp_name))
        command.force = None
        esb_channel.is_active = self.is_active
        esb_channel.path = self.channel_path
        esb_channel.save()

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


class Esb_edit_channel(Esb_channel_plugin):
    def __init__(self, request):
        super().__init__(request)
        self.body_data = json.loads(request.body.decode('utf-8'))
        self.im_channel_type = self.body_data.get('code', '')
        self.config_data = self.body_data.get('config', '')
        self.is_active = self.config_data.get('is_active') if 'is_active' in self.config_data else True
        self.built_in_mapping = {"weixin": "send_weixin", "mail": "send_mail", "sms": "send_sms", "voice": "send_voice_msg"}

    # 编辑消息通道参数
    def edit_channel(self):
        for channel in self.channels_in_database:
            if channel.extra_info:
                if self.im_channel_type == json.loads(channel.extra_info).get("type", "") or self.built_in_mapping.get(self.im_channel_type) == channel.component_name:
                    command = Command()
                    command.force = None
                    channel.is_active = self.is_active
                    self.cmp_name = channel.component_name

                    # 只更新存在于 comp_conf 数据中的键
                    # 更新原始配置中已存在的键值对
                    origin_comp_conf = json.loads(channel.comp_conf)
                    input_comp_conf = self.config_data.get("comp_conf_to_db", [])

                    # 创建一个字典，以 origin_comp_conf 中的键作为键，对应的值为 True
                    existing_keys = {item[0]: True for item in origin_comp_conf}

                    # 遍历 input_comp_conf 中的每个键值对，如果键存在于 existing_keys 中，则更新原始配置的值
                    for key, value in input_comp_conf:
                        if key in existing_keys:
                            for entry in origin_comp_conf:
                                if entry[0] == key:
                                    entry[1] = value  # 更新值

                    # 不允许修改extra_info
                    self.config_data.setdefault("extra_info", {"is_confapi": True, "label_en": f"{self.cmp_name}",
                                                 "suggest_method": self.channel_method})

                    self.config_data.update({
                        "path": self.channel_path,
                        "comp_conf_to_db": origin_comp_conf,
                        "method": self.channel_method
                    })

                    command.update_channel_by_config(channel, self.config_data, [], [])

                    # 数据库操作成功才更新mapping
                    self.update_mapping()

                    refresh_components_manager()

                    return JsonResponse({"success": True,
                                         "message": "edit successfully"})

        return JsonResponse({"success": False,
                             "message": "Can not find channel in database"})

    def delete_channel(self):
        for channel in self.channels_in_database:
            if channel.extra_info:
                if self.im_channel_type == json.loads(channel.extra_info).get("type", ""):
                    channel.delete()

                    # 删除插件包目录
                    plugin_dir = os.path.join(BASE_DIR, 'components', 'generic', 'templates', 'cmsi', 'plugins',
                                              str(json.loads(channel.extra_info).get('type')))
                    if os.path.exists(plugin_dir):
                        shutil.rmtree(plugin_dir)

                    refresh_components_manager()
                    return JsonResponse({"success": True,
                                         "message": "deleted successfully"})

        return JsonResponse({"success": False,
                             "message": f"Can not find channel in database, channel type is: {self.im_channel_type}"})
