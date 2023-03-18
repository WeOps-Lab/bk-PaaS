FROM python:3.6.8

WORKDIR /opt
COPY . .

RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple -r ./requirements.txt

ENV BK_ENV production