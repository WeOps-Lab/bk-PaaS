RELEASE_PATH=/opt/release/open_paas
rm -Rf $RELEASE_PATH
mkdir -p $RELEASE_PATH

cp -Rf /data/bkee/open_paas/apigw/ $RELEASE_PATH
cp -Rf ../blueking-console/backend $RELEASE_PATH/console
cp -Rf ./paas2/appengine $RELEASE_PATH
cp -Rf /data/bkee/open_paas/cert $RELEASE_PATH
cp -Rf ./paas2/esb $RELEASE_PATH
cp -Rf ./paas2/login $RELEASE_PATH
cp -Rf ./paas2/paas $RELEASE_PATH

cp -Rf /data/bkee/open_paas/projects.yaml $RELEASE_PATH
cp -Rf ./readme.md $RELEASE_PATH
cp -Rf ./VERSION $RELEASE_PATH

cp -Rf ./support-files $RELEASE_PATH

cp -r -n /data/bkee/open_paas/support-files/pkgs/* /opt/release/open_paas/support-files/pkgs/

cd /opt/release/open_paas/apigw
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs

cd ../esb
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs

cd ../paas
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs

cd ../appengine 
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs

cd ../console
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs

cd ../login
pip3 download -r requirements.txt --dest /opt/release/open_paas/support-files/pkgs