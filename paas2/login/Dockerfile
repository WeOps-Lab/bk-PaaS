FROM python:3.6.8

WORKDIR /apps
ADD ./paas2/login .

WORKDIR /apps/
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple -r ./requirements.txt

ENV BK_ENV production