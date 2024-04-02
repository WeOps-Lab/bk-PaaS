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

from django.conf.urls import include, url
from django.contrib import admin
from esb import views

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^c/", include("components.urls")),
    url(r"^", include("healthz.urls")),
    url(r'esb_channel_plugin/upload/', views.upload_file, name='upload_file'),    # url /upload/ maps to view `upload_file`
    url(r'esb_channel_plugin/edit/', views.edit_config, name='edit_config'),
    url(r'esb_channel_plugin/delete/', views.delete_config, name='delete_config'),
]


# 处理404和500请求
handler404 = "esb.views.handler_404_view"
handler500 = "esb.views.handler_500_view"
