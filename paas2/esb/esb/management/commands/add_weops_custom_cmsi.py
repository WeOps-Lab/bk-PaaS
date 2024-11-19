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
import logging

from django.core.management.base import BaseCommand

from common.constants import API_TYPE_Q
from esb.bkcore.models import ComponentSystem, ESBBuffetComponent, ESBChannel, SystemDocCategory
from esb.management.utils import conf_tools
from past.builtins import basestring

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """update system and channel data to db"""

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", dest="force", help="Force data update to db")

    def handle(self, *args, **options):
        self.force = options["force"]
        self.warning_msgs = []

        self.update_channels()

        for msg in self.warning_msgs:
            logger.warning(msg)

        logger.info("Add weops custom env done")

    def update_channels(self):

        conf_client = conf_tools.ConfClient()
        for system_name, channels in list(conf_client.channels.items()):
            if system_name == "CMSI":
                try:
                    system = ComponentSystem.objects.get(name=system_name)
                except ComponentSystem.DoesNotExist:
                    continue

                for channel in channels:
                    # 只更新短信、邮件、语音通知
                    if channel["path"] == "/cmsi/send_sms/" or channel["path"] == "/cmsi/send_mail/" or channel["path"] == "/cmsi/send_voice_msg/":
                        try:
                            esb_channel = ESBChannel.objects.get(path=channel["path"])
                        except ESBChannel.DoesNotExist:
                            continue
                        else:
                            is_hidden = channel.get("is_hidden", False)
                            is_deprecated = channel.get("is_deprecated", False)
                            is_hidden = is_hidden or is_deprecated

                            channel["name"] = channel["component_label"]
                            channel["type"] = 2 if channel["component_type"] == API_TYPE_Q else 1
                            channel["is_hidden"] = is_hidden
                            channel["component_system_id"] = system.id
                            channel["component_codename"] = channel["comp_codename"]
                            channel["extra_info"] = {
                                "is_confapi": channel.get("is_confapi", False),
                                "label_en": channel.get("label_en", ""),
                                "suggest_method": channel.get("suggest_method", ""),
                            }

                            # 将 `comp_conf` 解析为列表
                            channel["comp_conf"] = json.loads(esb_channel.comp_conf)

                            # 转换列表为字典以方便处理
                            comp_conf_dict = {item[0]: item[1] for item in channel["comp_conf"]}

                            # 查询并新增 "weops_custom_csmi", 如果其不存在
                            if "weops_custom_csmi" not in comp_conf_dict:
                                channel["comp_conf"].append(["weops_custom_csmi", "False"])

                                # 确保转换为 JSON 字符串时使用双引号
                                comp_conf_json = json.dumps(channel["comp_conf"], ensure_ascii=False)

                                # 更新 `channel["comp_conf"]`
                                channel["comp_conf"] = comp_conf_json
                                self._update_channel_by_config(esb_channel, channel, ["comp_conf"],"")
                                logger.info("id: %s, name: %s, path: %s update success" % (esb_channel.id, esb_channel.name, esb_channel.path))



    def diff_obj_conf(self, obj, conf, flag, default_update_fields, force_update_fields):
        info = []
        warning = []
        for fields, is_info_level in [(default_update_fields, True), (force_update_fields, self.force)]:
            for field in fields:
                if field not in conf:
                    continue
                if getattr(obj, field) != conf[field]:
                    msg = "%s: %s -> %s" % (field, getattr(obj, field), conf[field])
                    if is_info_level:
                        info.append(msg)
                    else:
                        warning.append(msg)
        if info:
            logger.info("%s changed: %s", flag, ", ".join(info))
        if warning:
            self.warning_msgs.append("%s change: %s" % (flag, ", ".join(warning)))

    def _update_channel_by_config(self, channel, config, default_update_fields, force_update_fields):
        self.diff_obj_conf(
            channel,
            config,
            "channel %s" % config["path"],
            default_update_fields,
            force_update_fields,
        )
        channel.method = config["method"]
        channel.extra_info = json.dumps(config["extra_info"])
        channel.__dict__.update(self.get_by_fields(config, default_update_fields))
        if channel.is_confapi:
            channel.comp_conf = json.dumps(config["comp_conf_to_db"])
        if self.force:
            channel.__dict__.update(self.get_by_fields(config, force_update_fields))

        try:
            channel.save()
        except Exception:
            logger.exception("update channel fail: id=%s, config=%s", channel.pk, json.dumps(config))

    def get_by_fields(self, obj, fields):
        return dict([(field, obj[field]) for field in fields if field in obj])