## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
正式环境配置
"""

DEBUG = False

# use the static root 'static' in production envs
if not DEBUG:
    STATIC_ROOT = 'static'

# 数据库配置信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'open_paas',
        'USER': '__BK_PAAS_MYSQL_USER__',
        'PASSWORD': '__BK_PAAS_MYSQL_PASSWORD__',
        'HOST': '__BK_PAAS_MYSQL_HOST__',
        'PORT': '__BK_PAAS_MYSQL_PORT__',
    },
    'bksuite': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bksuite_common',
        'USER': '__BK_PAAS_MYSQL_USER__',
        'PASSWORD': '__BK_PAAS_MYSQL_PASSWORD__',
        'HOST': '__BK_PAAS_MYSQL_HOST__',
        'PORT': '__BK_PAAS_MYSQL_PORT__',
    }
}

# domain
PAAS_DOMAIN = '__BK_PAAS_PUBLIC_ADDR__'
# inner domain, use consul domain,  for api
PAAS_INNER_DOMAIN = '__BK_PAAS_PRIVATE_ADDR__'
# schema = http/https, default http
HTTP_SCHEMA = '__BK_HTTP_SCHEMA__'
HTTP_SCHEMA = HTTP_SCHEMA or "http"

# 用户管理内部接口地址
BK_USERMGR_HOST="__BK_USERMGR_PRIVATE_ADDR__"

# 登陆服务地址
LOGIN_HOST = "http://__LAN_IP__:8003"

SECRET_KEY = '__BK_PAAS_ESB_SECRET_KEY__'

# cookie 名称
BK_COOKIE_NAME = 'bk_token'
# cookie有效期
BK_COOKIE_AGE = 60 * 60 * 24
# cookie访问域
BK_COOKIE_DOMAIN = '.__BK_DOMAIN__'

# ESB Token
ESB_TOKEN = '__BK_PAAS_APP_SECRET__'

# license
IS_CERTIFICATE_SVC_ENABLED = False
CERTIFICATE_DIR = '__BK_CERT_PATH__'
CERTIFICATE_SERVER_DOMAIN = '__BK_LICENSE_PRIVATE_ADDR__'

# host iam
HOST_IAM = '__IAM_HOST__:__IAM_PORT__'
HOST_IAM_NEW = '__BK_IAM_PRIVATE_ADDR__'

# PaaS3.0 的访问地址
BK_PAAS3_URL = '__BK_PAAS3_URL__'
# API 网关访问地址
BK_APIGW_URL = '__BK_APIGW_URL__'
# API 网关文档中心地址
BK_APIGW_DOC_URL = '__BK_APIGW_DOC_URL__'
