#!/usr/bin/env bash

export POETRY=/root/.local/bin/poetry
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
export COMICS_PATH=/usr/share/calvin/comics/
export SSH_USER=$(</usr/share/calvin/SSH_USER)
mv /home/$SSH_USER/.ssh/calvin.pub /home/$SSH_USER/.ssh/authorized_keys
chown -R $SSH_USER:$SSH_USER /home/$SSH_USER/.ssh/
mkdir /tmp/calvin_and_hobbes
cd /tmp/calvin_and_hobbes
dphys-swapfile swapoff
sed -ie 's/CONF_SWAPSIZE=.*$/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
git clone https://github.com/alliefitter/calvin_and_hobbes_viewer.git
cd calvin_and_hobbes_viewer
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
cp etc/.xsession /home/$SSH_USER/
cp etc/nginx/* /etc/nginx/conf.d
cp etc/systemd/* /etc/systemd/system/
cp scripts/xhost_calvin.sh /usr/bin/xhost-calvin
chmod +x /usr/bin/xhost-calvin
cd /app/calvin
virtualenv venv
./venv/bin/pip3 install *.whl
./venv/bin/calvin init-db
unzip /usr/share/calvin/comics.zip -d "$COMICS_PATH"
rm /usr/share/calvin/comics.zip
sed -ie 's/user .*$/user hobbes hobbes/g' /etc/nginx/nginx.conf
rm /etc/nginx/sites-enabled/*
chown -R calvin:calvin /app/calvin
chown -R hobbes:hobbes /app/hobbes
cp /tmp/calvin_and_hobbes/calvin_and_hobbes_viewer/scripts/xhost_calvin.sh /usr/bin/xhost_calvin
systemctl daemon-reload
systemctl enable calvin-api.service
systemctl enable calvin-daemon.service
systemctl enable calvin-daily.service
systemctl enable calvin-daily.timer
systemctl enable calvin-xhost.service
(cat >> /etc/lightdm/lightdm.conf)
raspi-config nonint do_boot_behaviour B4
(cat | tee -a /etc/lightdm/lightdm.conf  >/dev/null) << EOF
[SeatDefaults]
user-session=openbox
autologin-user=$SSH_USER
autologin-user-timeout=0
EOF
