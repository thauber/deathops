#!/bin/bash

set -eo pipefail

USER="$(id -un)"
GRP="$(id -gn)"

pushd $(dirname $0) > /dev/null
REPOPATH="$(pwd)"
REPOPATH="$(dirname $REPOPATH)"
popd > /dev/null

sudo apt-get install python-virtualenv

sudo rm -fR /deathops/ve /deathops/src

sudo mkdir -p /deathops/data /deathops/etc /deathops/log /deathops/run

sudo chown -R $USER:$GRP /deathops

ln -s $REPOPATH /deathops/src

virtualenv /deathops/ve
source /deathops/ve/bin/activate
ls -l $REPOPATH/requirements.in
/deathops/ve/bin/pip install -r $REPOPATH/requirements.txt

if [ "$(uname)" != "Darwin" ]; then
sudo adduser --disabled-password --gecos "" deathops || true
echo "deathops:$(uuidgen)" | sudo chpasswd
sudo chown -R deathops:deathops /deathops
sudo chown -R root:root /deathops/run
sudo cp $REPOPATH/init/supervisord.service /lib/systemd/system/supervisord.service
sudo systemctl enable supervisord
sudo -u deathops ssh-keygen -f /home/deathops/.ssh/charons-obol_rsa -N ""
ssh-copy-id -i ~/.ssh/mykey riverstyx@thauber.com
fi

sudo apt-get install openssh-server
sudo apt-get install autossh
sudo adduser --disabled-password --gecos "" charon || true
sudo -u charon ssh-keygen
sudo cp $REPOPATH/init/charon.service /lib/systemd/system/charon.service
sudo systemctl enable charon

curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

echo "Done."
