#!/usr/bin/env bash

#########################################
# Printer prerequisites
#########################################

# Install printer system dependencies
sudo apt-get update
sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python-serial python-pil python-unidecode -y

# # Install printer driver (CUPS filter). Disregard g++ warning.
git clone https://github.com/adafruit/zj-58
pushd zj-58
make
sudo ./install
popd

# # Make printer the default printer
# # Note the baud rate number may differ depending on printer
sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=19200 -m zjiang/ZJ-58.ppd
sudo lpoptions -d ZJ-58

# Test printer
# stty -F /dev/serial0 19200
# echo -e "This is a test.\\n\\n" > /dev/serial0

# Restart system
# sudo reboot

# Clone Adafruit Python Thermal Printer library repo
git clone git@github.com:adafruit/Python-Thermal-Printer.git
cp Python-Thermal-Printer/Adafruit_Thermal.py ../

#########################################
# Generally useful
#########################################

sudo apt-get install vim -y

#########################################
# NYT mini xword script prerequisites
#########################################

# Install nvm; node v14+ required
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bashrc
nvm install v14.4.0

# Needed for Puppeteer
sudo apt-get install chromium-browser -y

#########################################
# WIP: Run xword-printer script on rpi boot

# Script starts successfully but node subprocess not working

#########################################

# sudo cp xword-printer.service /lib/systemd/system/xword-printer.service
# sudo chmod 644 /lib/systemd/system/xword-printer.service
# sudo systemctl daemon-reload
# sudo systemctl enable xword-printer.service