#!/bin/bash

libcamera-vid -width 640 -height 480 -o -t 0 -b 2000000 | nc 172.25.32.1 5777