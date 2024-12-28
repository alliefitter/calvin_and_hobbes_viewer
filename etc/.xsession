#!/usr/bin/env bash

export DISPLAY=:0
xset -dpms
setterm -blank 0 -powerdown 0
xset s off
xhost + local:calvin
