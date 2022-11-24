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
        'ENGINE': 'django.db.backends.mysql',   # 默认用mysql
        'NAME': 'open_paas',
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

# cookie访问域
BK_COOKIE_DOMAIN = '.__BK_DOMAIN__'

# session in cookie secure; uncomment this if you need a secure cookie
# if HTTP_SCHEMA == "https":
#     SESSION_COOKIE_SECURE = True

# 用户管理内部接口地址
BK_USERMGR_HOST="__BK_USERMGR_PRIVATE_ADDR__"

SECRET_KEY = '__BK_PAAS_ESB_SECRET_KEY__'

# ESB Token
ESB_TOKEN = '__BK_PAAS_APP_SECRET__'

# license
CERTIFICATE_DIR = '__BK_CERT_PATH__'
CERTIFICATE_SERVER_DOMAIN = '__BK_LICENSE_PRIVATE_ADDR__'
