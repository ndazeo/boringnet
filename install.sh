#!/bin/bash

path=$(dirname $(realpath $0))

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
rm -f /etc/systemd/system/boring.service

if [[ "$1" -ne "--uninstall" ]]; then
    mkdir -p /usr/local/boringnet
    cp $path/boring.py /usr/local/boringnet
    if [[ ! -d "/usr/local/boringnet/config.yml" ]]; then
        cp $path/config.yml.example /usr/local/boringnet/config.yml
    fi;
    ln -s /usr/local/boringnet/boring.service /etc/systemd/system/boring.service
    chmod 664 /etc/systemd/system/boring.service
else
    rm -rf /usr/local/boringnet
fi;
systemctl daemon-reload