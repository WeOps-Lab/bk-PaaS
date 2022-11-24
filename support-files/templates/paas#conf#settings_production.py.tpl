## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
正式环境配置
"""
import environ

env = environ.Env()


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

# cookie 名称
BK_COOKIE_NAME = 'bk_token'
# cookie有效期
BK_COOKIE_AGE = 60 * 60 * 24
# cookie访问域
BK_COOKIE_DOMAIN = '.__BK_DOMAIN__'

# 控制台地址
ENGINE_HOST = "http://__LAN_IP__:8000"
# 登陆服务地址
LOGIN_HOST = "http://__LAN_IP__:8003"

# host for cc
HOST_CC = '__BK_CMDB_PUBLIC_ADDR__'
# host for job
HOST_JOB = '__BK_JOB_PUBLIC_ADDR__'

# host iam, should use the inner ip and port
HOST_IAM = '__IAM_HOST__:__IAM_PORT__'
HOST_IAM_NEW = '__BK_IAM_PRIVATE_ADDR__'

# host bkauth
HOST_BKAUTH = '__BK_AUTH_PRIVATE_ADDR__'

# 用户管理内部接口地址
BK_USERMGR_HOST="__BK_USERMGR_PRIVATE_ADDR__"

SECRET_KEY = '__BK_PAAS_ESB_SECRET_KEY__'

# ESB Token
ESB_TOKEN = '__BK_PAAS_APP_SECRET__'

# app env for deploy
APP_DEPLOY_ENVS = {
    # iam v2
    # 2020-01-03 change bk_iam_host to bk_iam_inner_host
    # "BK_IAM_HOST": bk_iam_inner_host,
    "BK_IAM_INNER_HOST": "%s://%s" % ("http", HOST_IAM),
    # iam v3
    "BK_IAM_V3_APP_CODE": "bk_iam",
    "BK_IAM_V3_INNER_HOST": "%s://%s" % ("http", HOST_IAM_NEW),
}


# 日志查询Elasticsearch服务器
ELASTICSEARCH_URLS = "__BK_PAAS_ES7_ADDR__"
ELASTICSEARCH_HOSTS = ELASTICSEARCH_URLS.split(";")

# 告警配置redis配置: 注意, paas目前仅告警redis, 牵连到日志, 所以暂时不使用sentinel模式
USE_SENTINEL = False
ALARM_REDIS_HOST = '__BK_PAAS_REDIS_HOST__'
ALARM_REDIS_PORT = __BK_PAAS_REDIS_PORT__
ALARM_REDIS_MASTER_NAME = ''
ALARM_REDIS_PASSWORD = '__BK_PAAS_REDIS_PASSWORD__'
ALARM_REDIS_CHANNEL = 'paas_app_alarm_config'

# for s3 storage
STORAGE_TYPE="__BK_PAAS_SHARED_STORAGE_TYPE__"
STORAGE_HOST = '__BK_PAAS_CEPH_HOST__'
STORAGE_PORT = '__BK_PAAS_CEPH_S3_PORT__'
if STORAGE_PORT.isdigit():
    STORAGE_PORT = int(STORAGE_PORT)
else:
    STORAGE_PORT = 7480
STORAGE_ACCESS_KEY = '__BK_PAAS_S3_ACCESS_KEY__'
STORAGE_SECRET_KEY = '__BK_PAAS_S3_SECRET_KEY__'
STORAGE_ADMIN_ENDPOINT = '/admin/'
STORAGE_TENANT = '__BK_PAAS_S3_UID__'

# PaaS3.0 的访问地址
BK_PAAS3_URL = '__BK_PAAS3_URL__'
# API 网关访问地址
BK_APIGW_URL = '__BK_APIGW_URL__'
# API 网关文档中心地址
BK_APIGW_DOC_URL = '__BK_APIGW_DOC_URL__'
# 是否隐藏菜单项：ESB 管理端的自助接入
BK_ESB_MENU_ITEM_BUFFET_HIDDEN = env.get_value(
    'BK_ESB_MENU_ITEM_BUFFET_HIDDEN',
    cast=bool,
    default='__BK_ESB_MENU_ITEM_BUFFET_HIDDEN__',
    parse_default=True,
)
