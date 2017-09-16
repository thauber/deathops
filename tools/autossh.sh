#!/bin/bash

# make sure autossh is installed first
# sudo apt-get install autossh

sudo -u mattb /usr/bin/autossh -M 10000 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -i /home/mattb/.ssh/id_rsa -R 2222:localhost:22 matt@vazor.com &
