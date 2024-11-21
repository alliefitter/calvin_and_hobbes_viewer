#!/usr/bin/env bash

xset -dpms
while true; do
  /usr/bin/xhost + local:calvin  < /dev/null && break
  sleep 5
done