#!/usr/bin/env bash

#if [[ ! -v COMICS_ZIP_PATH ]]; then
#  echo "COMICS_ZIP_PATH not set"
#  exit 1
#fi
export POETRY=/root/.local/bin/poetry
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
dphys-swapfile swapoff
sed -ie 's/CONF_SWAPSIZE=.*$/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
apt update
apt install nodejs npm nginx libjpeg-dev zlib1g-dev -y
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
#cp "$COMICS_ZIP_PATH" .
#unzip comics.zip -d comics/
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
