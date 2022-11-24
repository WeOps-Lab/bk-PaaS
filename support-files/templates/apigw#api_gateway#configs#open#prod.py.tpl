## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from .base import *  # noqa

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'open_paas',
        'USER': '__BK_PAAS_MYSQL_USER__',
        'PASSWORD': '__BK_PAAS_MYSQL_PASSWORD__',
        'HOST': '__BK_PAAS_MYSQL_HOST__',
        'PORT': '__BK_PAAS_MYSQL_PORT__',
    }
}

PLATFORM_DB_CONF_PAAS = {
    'NAME': 'open_paas',
    'ALIAS_NAME': 'bk_paas',
    'USER': '__BK_PAAS_MYSQL_USER__',
    'PASSWORD': '__BK_PAAS_MYSQL_PASSWORD__',
    'HOST': '__BK_PAAS_MYSQL_HOST__',
    'PORT': '__BK_PAAS_MYSQL_PORT__',
}

# Generic Django project settings
DEBUG = False
APP_CODE = 'bk_paas'
SECRET_KEY = '__BK_PAAS_APP_SECRET__'

# Redis settings
COMMON_REDIS_CONF = {
    'host': '__BK_PAAS_REDIS_HOST__',
    'port': '__BK_PAAS_REDIS_PORT__',
    'password': '__BK_PAAS_REDIS_PASSWORD__',
    'max_connections': 600,
    'db': 0,
}

# 频率控制的redis配置
REDIS_CONF_FOR_RATELIMIT = COMMON_REDIS_CONF

# cache采用的redis配置
REDIS_CONF_FOR_CACHE = COMMON_REDIS_CONF

# 负载均衡的redis配置
REDIS_CONF_FOR_LOADBLANCE = COMMON_REDIS_CONF

# IP白名单校验redis配置
REDIS_CONF_FOR_IPPERM = COMMON_REDIS_CONF


# 凭据管理系统（Secrets Manager，SSM）
BKSSM_HOST = "http://__BK_SSM_PRIVATE_ADDR__"
