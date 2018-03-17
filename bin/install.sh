#!/bin/bash

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
fi

sudo apt-get install openssh-server
sudo apt-get install autossh
sudo adduser --disabled-password --gecos "" charon || true
sudo -u charon ssh-keygen -f /home/charon/.ssh/obol_rsa -N ""
sudo ssh-copy-id -i /home/charon/.ssh/obol_rsa riverstyx@thauber.com

mkdir /home/deathball/gcp

curl https://sdk.cloud.google.com -o /home/deathball/gcp/install.sh
echo "Google Cloud Platform Downloaded."
/home/deathball/gcp/install.sh
echo "Google Cloud Platform Installed."
gcloud init
echo "Google Cloud Platform Initialized."

echo "Done."
