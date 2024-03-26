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

from esb.channel.plugin.utils import *
from esb.forms import UploadFileForm, EditForm, DeleteForm

from components.esb_conf import config
from components.generic.templates.cmsi.toolkit import configs as msg_config


def handler_404_view(request):
    resp = JsonResponse(
        {
            "result": False,
            "data": None,
            "message": "The content does not exist",
        },
        status=404,
    )
    return resp


def handler_500_view(request):
    resp = JsonResponse(
        {
            "result": False,
            "data": None,
            "message": "Request is abnormal, please contact the component developer",
        },
        status=500,
    )
    return resp


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            esb_plugin = Esb_channel_plugin(request)
            check_error = esb_plugin.handle_uploaded_file()
            if check_error:
                return check_error

            try:
                esb_plugin.create_esb_plugin_channel()
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)})
            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "code or file is invalid or empty"})


def edit_config(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
        config_data = body_data.get('config', '')
        code_data = body_data.get('code', '')

        form = EditForm({'config': config_data, 'code': code_data})
        if form.is_valid():
            edit_channel = Esb_edit_channel(request)
            err = edit_channel.edit_channel()
            if err:
                return err
            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "code or config is invalid or empty"})


def delete_config(request):
    if request.method == 'POST':
        form = DeleteForm({'code': json.loads(request.body.decode('utf-8')).get('code', '')})
        if form.is_valid():
            edit_channel = Esb_edit_channel(request)
            err = edit_channel.delete_channel()
            if err:
                return err
            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": f"code is invalid or empty"})
