auth:
  sid: '__BK_PAASAGENT_SID__'  # agent sid
  token: '__BK_PAASAGENT_TOKEN__' # agent token
settings:
  CONTROLLER_SERVER_URL: 'http://__BK_PAAS_PRIVATE_ADDR__' # App Engine地址
  CERTIFICATE_SERVER_URL: 'https://__BK_LICENSE_PRIVATE_ADDR__/certificate' # 鉴权中心url
  CERTIFICATE_FILE_PATH: __BK_CERT_PATH__
  BASE_APP_PATH: '__BK_HOME__/paas_agent'
  USE_PYPI: 'true'
  USE_DOCKER: 'true'
  UID: '__BK_BLUEKING_UID__'
  GID: '__BK_BLUEKING_GID__'
  IMAGE_NAME: '__BK_PAASAGENT_PYTHON2_IMAGE_NAME__'

  AGENT_LOG_PATH: __BK_HOME__/logs/paasagent/agent.log
  TEMPLATE_PATH: 'paas_agent/etc/templates'
  BUILD_PATH: 'paas_agent/etc/build'
  EXECUTE_TIME_LIMIT: 300
  PYTHON_PIP: '__BK_PAASAGENT_PYPI_URL__'

java_settings:
  IMAGE_NAME: '__BK_PAASAGENT_JAVA_IMAGE_NAME__' # like bkbase/java:1.0

python3_settings:
  IMAGE_NAME: '__BK_PAASAGENT_PYTHON3_IMAGE_NAME__' # like bkbase/python3:1.0

port: __BK_PAASAGENT_SERVER_PORT__
ip: '__LAN_IP__'
