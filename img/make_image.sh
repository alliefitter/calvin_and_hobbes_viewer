#!/usr/bin/env bash

export DIR="$(dirname "$(realpath "$0")")"
echo "$PI_USER" > SSH_USER
sudo sdm --customize \
  --plugin user:"adduser=$PI_USER|password=$PASS" \
  --plugin apps:"apps=@$DIR/apps" \
  --plugin L10n:host \
  --plugin disables:piwiz \
  --plugin network:"nmconn=$DIR/wifi.nmconnection" \
  --plugin runatboot:"script=$DIR/first_boot.sh|output=/var/log/calvin.first_boot.log|error=/var/log/calvin.first_boot.log" \
  --plugin copyfile:"from=$COMICS_ZIP_PATH|to=/usr/share/calvin/|mkdirif=true" \
  --plugin copyfile:"from=$PUBLIC_KEY_PATH|to=/home/$PI_USER/.ssh/|mkdirif=true" \
  --plugin copyfile:"from=$DIR/SSH_USER|to=/usr/share/calvin/|mkdirif=true" \
  --extend --xmb 6144 \
  --expand-root \
  --regen-ssh-host-keys \
  --restart \
  2024-11-19-raspios-bookworm-arm64-lite.img
sudo sdm --burn /dev/sda \
  --hostname calvinpi \
  --expand-root \
  2024-11-19-raspios-bookworm-arm64-lite.img
