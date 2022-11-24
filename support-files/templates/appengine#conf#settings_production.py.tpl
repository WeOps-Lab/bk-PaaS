# -*- coding: utf-8 -*-
"""
正式环境配置
"""

from conf.default import *

DEBUG = False

# Database
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

SECRET_KEY = '__BK_PAAS_ESB_SECRET_KEY__'

# etcd services, ETCD_SERVERS = (('192.168.1.1', 4001), ('192.168.1.2', 4001), ('192.168.1.3', 4001))
IS_ETCD_ON = False
ETCD_SERVERS = "(('127.0.0.1', 4001), )"

CONSUL_HTTP_PORT = '__BK_CONSUL_HTTP_PORT__'
CONSUL_SERVER_CA_CERT = '__BK_HOME__/cert/__BK_CONSUL_CA_FILE__'
CONSUL_CLIENT_CERT_FILE = '__BK_HOME__/cert/__BK_CONSUL_CLIENT_CERT_FILE__'
CONSUL_CLIENT_KEY_FILE = '__BK_HOME__/cert/__BK_CONSUL_CLIENT_KEY_FILE__'
CONSUL_HTTPS_PORT = '__BK_CONSUL_HTTPS_PORT__'
