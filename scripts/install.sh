#!/usr/bin/env bash

export POETRY=/root/.local/bin/poetry
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
dphys-swapfile swapoff
sed -ie 's/CONF_SWAPSIZE=.*$/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
apt update
apt install git nodejs npm nginx libjpeg-dev zlib1g-dev python3-virtualenv lightdm openbox -y
mkdir projects
cd ~/projects
git clone https://github.com/alliefitter/calvin_and_hobbes_viewer.git
cd calvin_and_hobbes_viewer
raspi-config nonint do_boot_behaviour B4
curl -sSL https://install.python-poetry.org | python3 -
$POETRY build
cd hobbes
npm install
npm run build
cd ../
sudo useradd -r -s /bin/false calvin
sudo useradd -r -s /bin/false hobbes
mkdir -p /app/calvin
mkdir /app/calvin/comics
mkdir /app/hobbes
cp dist/*.whl /app/calvin
cp -r hobbes/dist/* /app/hobbes
cp etc/nginx/* /etc/nginx/conf.d
cp etc/systemd/* /etc/systemd/system/
cp scripts/xhost_calvin.sh /usr/bin/xhost-calvin
cd /app/calvin
virtualenv venv
./venv/bin/pip3 install *.whl
unzip /usr/share/calvin/comics.zip -d comics/
rm /usr/share/calvin/comics.zip
sed -ie 's/user .*$/user hobbes hobbes/g' /etc/nginx/nginx.conf
rm /etc/nginx/sites-enabled/*
chown -R calvin:calvin /app/calvin
chown -R hobbes:hobbes /app/hobbes
systemctl daemon-reload
systemctl enable calvin-api.service
systemctl enable calvin-daemon.service
systemctl enable calvin-daemon.timer
systemctl enable calvin-daily.service
systemctl enable calvin-daily.timer
systemctl enable calvin-xhost.service
