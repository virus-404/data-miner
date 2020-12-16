#!/bin/bash
setup-timezone -z /usr/share/zoneinfo
echo "Setting up backup container..."
echo "0       0,12       *       *       *       run-parts /etc/periodic/6hour" >> /etc/crontabs/root 2>&1

