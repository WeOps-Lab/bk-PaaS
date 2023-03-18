PAAS_RELEASE_PATH=/opt/release/open_paas
PAAS_AGENT_RELEASE_PATH=/opt/release/paas_agent

VENV_PATH=/tmp/venv

.PHONY: all paas paas-agent

paas-agent:
	rm -Rf $(PAAS_AGENT_RELEASE_PATH)
	mkdir -p $(PAAS_AGENT_RELEASE_PATH)
	cd ./paas2/paasagent/ && make build

	cp -Rf ./paas2/paasagent/projects.yaml $(PAAS_AGENT_RELEASE_PATH)
	cp -Rf ./paas2/paasagent/README.md $(PAAS_AGENT_RELEASE_PATH)
	cp -Rf ./paas2/paasagent/support-files/ $(PAAS_AGENT_RELEASE_PATH)

	cp -Rf /data/bkee/paas_agent/support-files/images/ $(PAAS_AGENT_RELEASE_PATH)/support-files/images/
	cp -Rf /data/bkee/paas_agent/support-files/pkgs/ $(PAAS_AGENT_RELEASE_PATH)/support-files/pkgs/
	cp -Rf ./paas2/paasagent/VERSION $(PAAS_AGENT_RELEASE_PATH)
	
	mkdir -p $(PAAS_AGENT_RELEASE_PATH)/paas_agent
	mkdir -p $(PAAS_AGENT_RELEASE_PATH)/paas_agent/lib
	mkdir -p $(PAAS_AGENT_RELEASE_PATH)/paas_agent/bin

	cp -Rf ./paas2/paasagent/etc $(PAAS_AGENT_RELEASE_PATH)/paas_agent
	cp -Rf ./paas2/paasagent/bin/paas_agent $(PAAS_AGENT_RELEASE_PATH)/paas_agent/bin

paas:
	rm -Rf $(PAAS_RELEASE_PATH)
	mkdir -p $(PAAS_RELEASE_PATH)

	cp -Rf ../blueking-console/backend $(PAAS_RELEASE_PATH)/console
	cp -Rf ./paas2/appengine $(PAAS_RELEASE_PATH)
	cp -Rf ./paas2/esb $(PAAS_RELEASE_PATH)
	cp -Rf ./paas2/login $(PAAS_RELEASE_PATH)
	cp -Rf ./paas2/paas $(PAAS_RELEASE_PATH)
	cp -Rf ./projects.yaml $(PAAS_RELEASE_PATH)
	cp -Rf ./readme.md $(PAAS_RELEASE_PATH)
	cp -Rf ./VERSION $(PAAS_RELEASE_PATH)
	cp -Rf ./support-files $(PAAS_RELEASE_PATH)
	
	virtualenv $(VENV_PATH) -p python3
	$(VENV_PATH)/bin/pip3 install setuptools==57.5.0
	
	$(VENV_PATH)/bin/pip3 download -r $(PAAS_RELEASE_PATH)/esb/requirements.txt --dest $(PAAS_RELEASE_PATH)/support-files/pkgs
	$(VENV_PATH)/bin/pip3 download -r $(PAAS_RELEASE_PATH)/paas/requirements.txt --dest $(PAAS_RELEASE_PATH)/support-files/pkgs
	$(VENV_PATH)/bin/pip3 download -r $(PAAS_RELEASE_PATH)/appengine/requirements.txt --dest $(PAAS_RELEASE_PATH)/support-files/pkgs
	$(VENV_PATH)/bin/pip3 download -r $(PAAS_RELEASE_PATH)/console/requirements.txt --dest $(PAAS_RELEASE_PATH)/support-files/pkgs
	$(VENV_PATH)/bin/pip3 download -r $(PAAS_RELEASE_PATH)/login/requirements.txt --dest $(PAAS_RELEASE_PATH)/support-files/pkgs

	rm -Rf $(VENV_PATH)

release-docker:
	cd ./paas2/appengine &&\
	docker build -t appengine . &&\
	cd ../esb &&\
	docker build -t esb . &&\
	cd ../login &&\
	docker build -t login . &&\
	cd ../paas &&\
	docker build -t paas . &&\
	cd ../paasagent  &&\
	docker build -t paasagent .