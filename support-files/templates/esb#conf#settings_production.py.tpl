## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from .default import *  # noqa: F403,F401

# Generic Django project settings
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

# Log settings
LOG_LEVEL = 'INFO'

SECRET_KEY = '__BK_PAAS_ESB_SECRET_KEY__'

# esb app_token
ESB_TOKEN = '__BK_PAAS_APP_SECRET__'

# esb ssl root dir
SSL_ROOT_DIR = '__BK_CERT_PATH__'

# paas host
PAAS_HOST = '__BK_PAAS_PRIVATE_ADDR__'

# Third party system host
# host for bk login
HOST_BK_LOGIN = '__BK_PAAS_PRIVATE_ADDR__'

# host for cc
HOST_CC = '__CMDB_HOST__:__CMDB_HTTP_PORT__'

# host for cc v3
HOST_CC_V3 = '__BK_CMDB_API_PRIVATE_ADDR__'

# host for job, default 80 for http/8443 for https
HOST_JOB = '__BK_JOB_GATEWAY_HTTPS_PRIVATE_ADDR__'

# host for gse, default 80 for http/8443 for https
HOST_GSE = '__BK_GSE_CACHE_APISERVER_ADDR__'

# host for gse proc
GSE_PROC_HOST = '__BK_GSE_PROC_ADDR__'
GSE_PROC_PORT = '__BK_GSE_PROC_PORT__'

# host for gse cacheapi
GSE_CACHEAPI_HOST = '__BK_GSE_CACHE_APISERVER_HOST__'
GSE_CACHEAPI_PORT = '__BK_GSE_CACHE_APISERVER_PORT__'

# host for gse process management service
GSE_PMS_HOST = '__BK_GSE_PMS_ADDR__'

# host for gse config
BK_GSE_CONFIG_ADDR = '__BK_GSE_CONFIG_ADDR__'

# host for DATA，数据平台监控告警系统, default 80 for http/8443 for https
HOST_DATA = '__DATAAPI_HOST__:__DATAAPI_PORT__'

# host for DATA BKSQL service
DATA_BKSQL_HOST = '__BKSQL_HOST__:__BKSQL_PORT__'

# host for DATA PROCESSORAPI
DATA_PROCESSORAPI_HOST = '__PROCESSORAPI_HOST__:__PROCESSORAPI_PORT__'

# host for DATA Modelflow service
DATA_MODELFLOW_HOST = '__MODELFLOW_HOST__:__MODELFLOW_API_PORT__'

# host for data v3
DATAV3_AUTHAPI_HOST = "__BKDATA_AUTHAPI_HOST__:__BKDATA_AUTHAPI_PORT__"
DATAV3_ACCESSAPI_HOST = "__BKDATA_ACCESSAPI_HOST__:__BKDATA_ACCESSAPI_PORT__"
DATAV3_DATABUSAPI_HOST = "__BKDATA_DATABUSAPI_HOST__:__BKDATA_DATABUSAPI_PORT__"
DATAV3_DATAFLOWAPI_HOST = "__BKDATA_DATAFLOWAPI_HOST__:__BKDATA_DATAFLOWAPI_PORT__"
DATAV3_DATAMANAGEAPI_HOST = "__BKDATA_DATAMANAGEAPI_HOST__:__BKDATA_DATAMANAGEAPI_PORT__"
DATAV3_DATAQUERYAPI_HOST = "__BKDATA_DATAQUERYAPI_HOST__:__BKDATA_DATAQUERYAPI_PORT__"
DATAV3_METAAPI_HOST = "__BKDATA_METAAPI_HOST__:__BKDATA_METAAPI_PORT__"
DATAV3_STOREKITAPI_HOST = "__BKDATA_STOREKITAPI_HOST__:__BKDATA_STOREKITAPI_PORT__"
DATAV3_BKSQL_HOST = "__BKDATA_BKSQL_HOST__:__BKDATA_BKSQL_PORT__"
DATAV3_MODELAPI_HOST = "__BKDATA_MODELAPI_HOST__:__BKDATA_MODELAPI_PORT__"
DATAV3_DATACUBEAPI_HOST = "__BKDATA_DATACUBEAPI_HOST__:__BKDATA_DATACUBEAPI_PORT__"
DATAV3_ALGORITHMAPI_HOST = "__BKDATA_MODELFLOWAPI_HOST__:__BKDATA_MODELFLOWAPI_PORT__"
DATAV3_DATALABAPI_HOST = "__BKDATA_DATALABAPI_HOST__:__BKDATA_DATALABAPI_PORT__"
DATAV3_AIOPSAPI_HOST = "__BKDATA_AIOPSAPI_HOST__:__BKDATA_AIOPSAPI_PORT__"
DATAV3_RESOURCECENTERAPI_HOST = "__BKDATA_RESOURCECENTERAPI_HOST__:__BKDATA_RESOURCECENTERAPI_PORT__"

# host for fta,  default 80 for http/8443 for https
HOST_FTA = '__BK_FTA_API_ADDR__'

# Redis config
USE_SENTINEL = False
REDIS_HOST = '__BK_PAAS_REDIS_HOST__'
REDIS_PORT = __BK_PAAS_REDIS_PORT__
REDIS_PASSWORD = '__BK_PAAS_REDIS_PASSWORD__'
REDIS_MASTER_NAME = ''

# devops
DEVOPS_HOST = '__DEVOPS_HOST__:__DEVOPS_PORT__'

# cicdkit
CICDKIT_HOST = '__CICDKIT_FQDN__:__CICDKIT_DCLOUD_PORT__'

# monitor
MONITOR_HOST = '__BKMONITOR_MONITOR_HOST__:__BKMONITOR_MONITOR_KERNELAPI_PORT__'
MONITOR_V3_HOST = '__BK_MONITOR_KERNELAPI_ADDR__'

# user_manage
USERMGR_HOST = '__BK_USERMGR_PRIVATE_ADDR__'

# bk_log
BK_LOG_HOST = '__BK_BKLOG_API_ADDR__'

# nodeman
NODEMAN_HOST = '__BK_NODEMAN_API_ADDR__'

# bscp
BK_BSCP_API_ADDR = '__BK_BSCP_API_ADDR__'

# bk-ssm
BK_SSM_API_URL = '__BK_SSM_PRIVATE_ADDR__'
BK_SSM_ACCESS_TOKEN_CACHE_MAXSIZE = 2000
BK_SSM_ACCESS_TOKEN_CACHE_TTL_SECONDS = 300

# bk_login bk-token cache
BK_TOKEN_CACHE_MAXSIZE = 2000
BK_TOKEN_CACHE_TTL_SECONDS = 60