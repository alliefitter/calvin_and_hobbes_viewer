#!/usr/bin/env bash

if ! command -v sdm >/dev/null 2>&1; then
  curl -L https://raw.githubusercontent.com/gitbls/sdm/master/EZsdmInstaller | bash
fi
if [ -f 2024-11-19-raspios-bookworm-arm64-lite.img ]; then
  rm 2024-11-19-raspios-bookworm-arm64-lite.img
fi
wget https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2024-11-19/2024-11-19-raspios-bookworm-arm64-lite.img.xz
unxz 2024-11-19-raspios-bookworm-arm64-lite.img.xz
