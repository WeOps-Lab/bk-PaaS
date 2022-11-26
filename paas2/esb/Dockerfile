FROM python:3.6.8

WORKDIR /apps
ADD ./paas2/esb .

WORKDIR /apps/
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  -r ./requirements.txt

ENV BK_ENV production