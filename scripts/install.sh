#!/usr/bin/env bash


if [ -z ${SHARE_PATH+x} ]; then
  export SHARE_PATH=/usr/share/calvin/
fi
if [ -z ${LIB_PATH+x} ]; then
  export LIB_PATH=/usr/lib/calvin/
fi

export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
export POETRY=/root/.local/bin/poetry
export COMICS_PATH=$SHARE_PATH/comics/
export SSH_USER=$(<$SHARE_PATH/SSH_USER)
echo "Using ssh user $SSH_USER"
echo "User lib path $LIB_PATH"
echo "User share path $SHARE_PATH"

mv /home/$SSH_USER/.ssh/calvinpi.pub /home/$SSH_USER/.ssh/authorized_keys
chown -R $SSH_USER:$SSH_USER /home/$SSH_USER/.ssh/
dphys-swapfile swapoff
sed -ie 's/CONF_SWAPSIZE=.*$/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

echo "Checkout lib"
mkdir -p $LIB_PATH
cd $LIB_PATH
git clone https://github.com/alliefitter/calvin_and_hobbes_viewer.git
cd calvin_and_hobbes_viewer

echo "Build calvin"
curl -sSL https://install.python-poetry.org | python3 -
$POETRY build

echo "Build hobbes"
cd hobbes
npm install
npm run build
cd ../

echo "Adding users"
sudo useradd -r -s /bin/false calvin
sudo useradd -r -s /bin/false hobbes

echo "Deploying"
mkdir -p /app/calvin
mkdir /app/hobbes
mkdir /etc/lightdm/lightdm.conf.d/
cp dist/*.whl /app/calvin
cp -r hobbes/dist/* /app/hobbes
cp etc/nginx/* /etc/nginx/conf.d
cp etc/systemd/* /etc/systemd/system/
cp etc/lightdm/10-calvin.conf /etc/lightdm/lightdm.conf.d/
sed -ie "s/SSH_USER/$SSH_USER/g" /etc/lightdm/lightdm.conf.d/10-calvin.conf
cp scripts/xhost_calvin.sh /usr/bin/xhost-calvin
chmod +x /usr/bin/xhost-calvin

echo "Installing calvin"
cd /app/calvin
virtualenv venv
./venv/bin/pip3 install *.whl
unzip $SHARE_PATH/comics.zip -d "$COMICS_PATH"
./venv/bin/calvin init-db
rm "${SHARE_PATH}comics.zip"

echo "Set up nginx"
sed -ie 's/user .*$/user hobbes hobbes;/g' /etc/nginx/nginx.conf
rm /etc/nginx/sites-enabled/*

echo "Changing app ownership"
chown -R calvin:calvin /app/calvin
chown -R hobbes:hobbes /app/hobbes
echo "Deployment complete"

echo "Setting up systemd "
systemctl daemon-reload
systemctl enable calvin-api.service
systemctl enable calvin-daemon.service
systemctl enable calvin-daily.service
systemctl enable calvin-daily.timer
systemctl enable calvin-xhost.service
raspi-config nonint do_boot_behaviour B4
echo "Installation complete!"
