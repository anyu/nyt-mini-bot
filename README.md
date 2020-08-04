# NYT Mini Bot


## Tools used
- Raspberry Pi 3 Model B with Raspian Buster image
- [Adafruit Mini Thermal Receipt Printer Starter Pack](https://www.adafruit.com/product/600)
- Micro SD card
- Ethernet cable

## Requirements
- node v14+

## Process

### Set up Raspberry Pi
1. Flash [Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/) image to micro SD card with (Etcher)[https://www.balena.io/etcher/])
1. Enable SSH on the rpi

### Connect and configure rpi to printer
1. Follow Adafruit’s [Thermal Printer configuration tutorial](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer)


### xword-fetcher.js script
1. Using [Puppeteer](https://github.com/puppeteer/puppeteer), this Node script navigates to the NYT Mini page, takes a screenshot of the crossword board, and saves the clues to a text file.

### xword-printer.py script
1. This Python script executes the xword-fetcher script, connects to the thermal printer using the [Adafruit Python Thermal Printer library](https://github.com/adafruit/Python-Thermal-Printer), and prints out the crossword board/clues retrieved by xword-fetcher.