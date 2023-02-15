RELEASE_PATH=/opt/release/paas_agent
rm -Rf $RELEASE_PATH
mkdir -p $RELEASE_PATH

cd ./paas2/paasagent/
make build

cp -Rf ./projects.yaml $RELEASE_PATH
cp -Rf ./README.md $RELEASE_PATH
cp -Rf /data/bkee/paas_agent/support-files/ $RELEASE_PATH
cp -Rf ./VERSION $RELEASE_PATH
mkdir -p $RELEASE_PATH/paas_agent
mkdir -p $RELEASE_PATH/paas_agent/lib
cp -Rf ./etc $RELEASE_PATH/paas_agent
mkdir -p $RELEASE_PATH/paas_agent/bin
cp -Rf ./bin/paas_agent $RELEASE_PATH/paas_agent/bin