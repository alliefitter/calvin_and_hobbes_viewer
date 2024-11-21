#!/usr/bin/env bash

dphys-swapfile swapoff
sed -ie 's/CONF_SWAPSIZE=.*$/CONF_SWAPSIZE=2048/g'
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
apt install nodejs npm nginx
curl -sSL https://install.python-poetry.org | python3 -
cd calvin
poetry build
cd ../
cd hobbes
npm install
npm build
cd ../
sudo useradd -r -s /bin/false calvin
sudo useradd -r -s /bin/false hobbes
mkdir -p /app/calvin
mkdir /app/calvin/comics
mkdir /app/hobbes
cp dist/*.whl /app/calvin
cp hobbes/dist/* /app/hobbes
cp etc/nginx/* /etc/nginx/conf.d
cp etc/systemd/* /etc/systemd/system/
cp scripts/xhost_calvin.sh /usr/bin/xhost-calvin
cd /app/calvin
virtualenv venv
./venv/bin/pip3 install *.whl
cp /boot/comics.zip .
unzip comics.zip -d comics/
sed -ie 's/user .*$/user hobbes hobbes/g' /etc/nginx/nginx.conf
rm /etc/nginx/site-enabled/*
chown -R calvin:calvin /app/calvin
chown -R hobbes:hobbes /app/hobbes
systectl daemon-reload
systemctl enable calvin-api.service
systemctl enable calvin-daemon.service
systemctl enable calvin-daemon.timer
systemctl enable calvin-daily.service
systemctl enable calvin-daily.timer
systemctl enable calvin-xhost.service
