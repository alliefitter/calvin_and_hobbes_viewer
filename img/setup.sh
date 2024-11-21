#!/usr/bin/env bash

curl -L https://raw.githubusercontent.com/gitbls/sdm/master/EZsdmInstaller | bash
wget https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2024-11-19/2024-11-19-raspios-bookworm-arm64-lite.img.xz
unxz 2024-11-19-raspios-bookworm-arm64-lite.img.xz
