#!/bin/bash

set -eo pipefail

USER="$(id -un)"
GRP="$(id -gn)"

pushd $(dirname $0) > /dev/null
REPOPATH="$(pwd)"
REPOPATH="$(dirname $REPOPATH)"
popd > /dev/null

rm -fR /deathops/ve /deathops/src

sudo mkdir -p /deathops/data /deathops/etc /deathops/log /deathops/run

sudo chown -R $USER:$GRP /deathops

ln -s $REPOPATH /deathops/src

virtualenv /deathops/ve
source /deathops/ve/bin/activate
ls -l $REPOPATH/requirements.in
/deathops/ve/bin/pip install -r $REPOPATH/requirements.txt

if [ "$(uname)" != "Darwin" ]; then
sudo adduser --disabled-password --gecos "" deathops
echo "deathops:$(uuidgen)" | sudo chpasswd
sudo cp $REPOPATH/init/supervisord.service /lib/systemd/system/supervisord.service
sudo systemctl enable supervisord
fi
