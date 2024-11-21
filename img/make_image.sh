#!/usr/bin/env bash

export DIR="$(dirname "$(realpath "$0")")"
sudo sdm --customize \
  --plugin user:"adduser=$USER|password=$PASSWORD" \
  --plugin L10n:host \
  --plugin disables:piwiz \
  --plugin sshkey:"sshuser=$USER|keyname=calvinpi|import-key=$SSH_KEY|authkey=true" \
  --plugin network:"nmconn=$DIR/wifi.nmconnection" \
  --plugin runatboot:"script=$DIR/first_boot.sh|output=/dev/stdout|error=/var/log/first_boot.error.log" \
  --plugin copyfile:"from=$COMICS_ZIP_PATH|to=/usr/share/calvin/|mkdirif=true" \
  --extend --xmb 6144 \
  --expand-root \
  --regen-ssh-host-keys \
  --restart \
  2024-11-19-raspios-bookworm-arm64-lite.img
sudo sdm --burn /dev/sda \
  --hostname calvinpi \
  --expand-root \
  2024-11-19-raspios-bookworm-arm64-lite.img
