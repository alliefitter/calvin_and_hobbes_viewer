#!/usr/bin/env bash

export DIR="$(dirname "$(realpath "$0")")"
sudo sdm --customize \
  --plugin user:"adduser=$USER|password=$PASSWORD" \
  --plugin L10n:host \
  --plugin disables:piwiz \
  --plugin sshkey:"sshuser=$USER|keyname=calvinpi" \
  --plugin network:"ifname=wlp3s0|cname=wlan2|ctype=wifi|wifi-ssid=$WIFI_SSID|wifi-password=$WIFI_PASS|wificountry=US" \
  --plugin runatboot:"script=$DIR/first_boot.sh" \
  --plugin copyfile:"from=$COMICS_ZIP_PATH|to=/usr/share/calvin/comics.zip|mkdirif" \
  --extend --xmb 6144 \
  --expand-root \
  --regen-ssh-host-keys \
  --restart \
  2024-11-19-raspios-bookworm-arm64-lite.img
#sudo sdm --burn /dev/sda \
#  --hostname calvinpi \
#  --expand-root \
#  2024-11-19-raspios-bookworm-arm64-lite.img.xz
