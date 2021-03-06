# NYT Mini Bot
Oh, hi. I'm a little pi bot that prints out the [New York Times Mini Crossword](https://www.nytimes.com/crosswords/game/mini) of the day for your analog xwordin' delight.

My creation was inspired by the [Vomit Comic Robot](https://imgur.com/a/hhrnQoC#TblkXme).

![NYT Mini Bot image](images/nyt-mini-bot1.jpg)
![NYT Mini Bot image](images/nyt-mini-bot2.jpg)
![NYT Mini Bot demo gif](images/demo.gif)

## Make me at home!

### Hardware
- Raspberry Pi (any model should work, I used a [3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b))
- [Adafruit Mini Thermal Receipt Printer Starter Pack](https://www.adafruit.com/product/600)
- micro SD card
- 5V 2A Micro USB AC Charger Power Supply Adapter
- ethernet cable
- basic Pi case (dependent on model, I used [this](https://www.amazon.com/gp/product/B00MQLB1N6/) one)

*For button and light functionality*
- LED
- push button
- female-to-male jumper wires x4
- resistor
- solderless breadboard

![materials](images/materials.jpg)

### Headless Raspberry Pi + thermal printer setup
1. Flash a [Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/) image (the full version, not lite) to micro SD card with [Etcher](https://www.balena.io/etcher)
1. Enable SSH on the rpi by adding a blank `ssh` file in the `/boot` directory of the SD card
1. Connect the rpi power supply and insert the SD card
1. Connect ethernet cable between the rpi and router
1. SSH into the rpi
1. Follow [Adafruit’s tutorial](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer) to connect and configure the rpi to the printer

### LED and button wiring
Wire up the LED, button, and resistor as follows:  

![breadboard diagram](images/bboard-diagram.jpg)

#### Helpful Resources
- [GPIO pin diagram](https://www.raspberrypi.org/documentation/usage/gpio/)
- [PiHut tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins) explains the concepts behind wiring up the breadboard

### NYT Mini Bot scripts
*Requirements: npm, Node v14+, Python 3.7+ (pre-installed on newer rpi OS images)*

1. SSH into the rpi and clone this repo
1. Run `./install.sh` (note: the first sections of this install script overlaps with the printer tutorial steps from above; can skip. Just make sure the `Python-Thermal-Printer/Adafruit_Thermal.py` file is copied within the nyt-mini-bot repo)
1. Run `./xword-printer.py`
1. Press the button!

---

#### xword-fetcher.js script
Using [Puppeteer](https://github.com/puppeteer/puppeteer), this Node script navigates to the NYT Mini page, takes a screenshot of the crossword board, and saves the date/clues to a text file.

To test in isolation:

1. If outside of the pi, remove `executablePath: 'chromium-browser',` from the `puppeteer.launch` line
1. Run `npm run start`

#### xword-printer.py script
This Python script executes the xword-fetcher script as a subprocess, connects to the printer using the [Adafruit Python Thermal Printer library](https://github.com/adafruit/Python-Thermal-Printer), and prints out the puzzle retrieved by xword-fetcher.



## Bonus

### Craft a shell for your printer
![NYT Mini Bot - custom shell](images/nyt-mini-bot-shell.jpg)
*material: shoebox*

### Other improvements
TODO:
- Trigger xword-printer.py script on rpi boot
- Get WiFi working on rpi