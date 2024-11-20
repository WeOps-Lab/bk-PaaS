# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS
Community Edition) available.
Copyright (C) 2017-2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import json

from common.django_utils import JsonResponse

from components.component import Component, SetupConfMixin
from common.constants import API_TYPE_Q, HTTP_METHOD
from common.base_utils import str_bool
from esb.bkcore.models import ComponentSystem, ESBChannel
from components.generic.templates.cmsi.toolkit import configs as msg_type_config
from esb.channel.plugin.utils import built_in_mapping
from .toolkit import configs
from .toolkit.tools import get_base64_icon


class GetMsgType(Component, SetupConfMixin):
    suggest_method = HTTP_METHOD.GET
    label = u"查询消息发送类型"
    label_en = "Get message type"

    sys_name = configs.SYSTEM_NAME
    api_type = API_TYPE_Q

    def handle(self):
        bk_language = self.request.headers.get("Blueking-Language", "en")
        esb_conf = self.request.kwargs.get("comp_conf")
        msg_type = []
        built_in_channel_path = []
        system_id = ComponentSystem.objects.get(name=msg_type_config.SYSTEM_NAME).id
        channels = ESBChannel.objects.filter_channels([system_id], is_hidden=None, is_active=None)

        for mt in configs.msg_type:
            is_active = "true" if channels.get(path=mt["path"]).is_active == 1 else "false"
            msg_type_entry = {
                **({"name": mt["name"]} if "name" in mt else {}),
                "type": mt["type"],
                # "icon": mt["active_icon"] if is_active else mt["unactive_icon"],
                "label": mt["label_en"] if bk_language == "en" else mt["label"],
                "is_active": is_active,
                **({"path": mt["path"]} if "path" in mt else {}),
                **({"method": mt["method"]} if "method" in mt else {}),
                **({"is_builtin": mt["is_builtin"]} if "is_builtin" in mt else {}),
            }
            built_in_channel_path.append(mt["path"]) # 记录内置消息能力路径

            if not esb_conf:
                msg_type_entry["icon"] = mt["active_icon"] if is_active else mt["unactive_icon"]

            # 查询消息能力配置参数
            if esb_conf:
                component_name = built_in_mapping.get(mt["type"])
                if component_name:
                    try:
                        channel = ESBChannel.objects.get(component_name=component_name)
                        comp_conf_to_db = json.loads(channel.comp_conf)
                    except ESBChannel.DoesNotExist:
                        comp_conf_to_db = None
                    msg_type_entry["comp_conf_to_db"] = comp_conf_to_db

            msg_type.append(msg_type_entry)

        if self.request.kwargs.get("im_channel"):
            # 补充IM消息通道字段
            for channel in channels:
                if channel.extra_info:
                    mapping = json.loads(channel.extra_info)
                    if mapping.get("type") and channel.path not in built_in_channel_path:  # 仅展示有type的消息通道且不在内置消息通道路径的
                        im_msg_type_entry = {
                            "name": channel.name,
                            "type": mapping.get("type", ""),
                            "label": mapping.get("label_en", mapping.get("type", "")) if bk_language == "en" else mapping.get("label", ""),
                            "is_active": "true" if channel.is_active == 1 else "false",
                            "path": channel.path,
                            "method": mapping.get("method", "POST"),
                            "is_builtin": mapping.get("is_builtin", "true"),
                        }

                        if not esb_conf:
                            im_msg_type_entry["icon"] = get_base64_icon(
                                "icons_v2/default_active.ico") if channel.is_active == 1 else get_base64_icon(
                                "icons_v2/default_unactive.ico")

                        if esb_conf:
                            im_msg_type_entry["comp_conf_to_db"] = json.loads(channel.comp_conf)

                        msg_type.append(im_msg_type_entry)

        self.response.payload = {
            "result": True,
            "data": msg_type,
        }
