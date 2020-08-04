# NYT Mini Bot
Oh, hi. I'm a little pi bot that prints out the [New York Times Mini Crossword](https://www.nytimes.com/crosswords/game/mini) of the day for your on-the-go crosswording needs.

My creation was inspired by the [Vomit Comic Robot](https://imgur.com/a/hhrnQoC#TblkXme).

## Tools used
- Raspberry Pi 3 Model B with Raspian Buster image
- [Adafruit Mini Thermal Receipt Printer Starter Pack](https://www.adafruit.com/product/600)
- Micro SD card
- Ethernet cable

## Requirements
- node v14+

### Raspberry Pi setup
1. Flash [Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/) image to micro SD card with [Etcher](https://www.balena.io/etcher)
1. Enable SSH on the rpi
1. Follow [Adafruit’s tutorial](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer) to connect and configure the rpi to the printer.

### xword-fetcher.js script
Using [Puppeteer](https://github.com/puppeteer/puppeteer), this Node script navigates to the NYT Mini page, takes a screenshot of the crossword board, and saves the clues to a text file.

### xword-printer.py script
This Python script executes the xword-fetcher script, connects to the thermal printer using the [Adafruit Python Thermal Printer library](https://github.com/adafruit/Python-Thermal-Printer), and prints out the crossword board/clues retrieved by xword-fetcher.