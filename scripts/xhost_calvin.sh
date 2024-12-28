#!/usr/bin/env bash

xset -dpms
setterm -blank 0 -powerdown 0
xset s off
while true; do
  /usr/bin/xhost + local:calvin  < /dev/null && break
  sleep 5
done