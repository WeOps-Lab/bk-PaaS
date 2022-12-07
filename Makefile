release:
	rm -Rf /opt/open_paas    &&\
	mkdir -p /opt/open_paas &&\
	cp -Rf ./paas2/appengine /opt/open_paas &&\
	pip3 download  -i https://mirrors.cloud.tencent.com/pypi/simple -r ./paas2/appengine/requirements.txt -d /opt/open_paas/support-files/pkgs &&\
	cp -Rf ./paas2/esb /opt/open_paas &&\
	pip3 download  -i https://mirrors.cloud.tencent.com/pypi/simple -r ./paas2/esb/requirements.txt -d /opt/open_paas/support-files/pkgs &&\
	cp -Rf ./paas2/login /opt/open_paas &&\
	pip3 download  -i https://mirrors.cloud.tencent.com/pypi/simple -r ./paas2/login/requirements.txt -d /opt/open_paas/support-files/pkgs &&\
	cp -Rf ./paas2/paas /opt/open_paas &&\
	pip3 download  -i https://mirrors.cloud.tencent.com/pypi/simple -r ./paas2/paas/requirements.txt -d /opt/open_paas/support-files/pkgs &&\
	cp -Rf ../blueking-console/backend /opt/open_paas/console &&\
	pip3 download  -i https://mirrors.cloud.tencent.com/pypi/simple -r ../blueking-console/backend/requirements.txt -d /opt/open_paas/support-files/pkgs &&\
	cp -Rf ./VERSION /opt/open_paas &&\
	cp -Rf ./readme.md  /opt/open_paas &&\
	cp -Rf ./projects.yaml /opt/open_paas &&\
	cp -Rf ./support-files /opt/open_paas &&\
	cd /opt/  &&\
	tar -zcvf ./open_paas_ce-2.14.33-bkofficial.tar.gz open_paas/