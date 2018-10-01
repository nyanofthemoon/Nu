#!/usr/bin/env bash

cd /home/pi/Nu && adb devices & sudo sudo python3.7 nu/webapp/server.py & python3.7 -m nu -vv