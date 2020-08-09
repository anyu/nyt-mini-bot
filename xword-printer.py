#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
from subprocess import Popen, PIPE
import os, sys, logging
import RPi.GPIO as GPIO

# Printer configs (dependent on printer)
SERIAL_PORT = "/dev/serial0"
PRINTER_BAUD_RATE = 19200

# Expected file paths
LOGO_PATH = "images/nyt_logo.png"
BOARD_PATH = "xwd_board.png"
PUZZLE_TEXT_PATH = "puzzle.txt"

# GPIO pins (BCM numbers)
LED_BUTTON = 20
PRINT_BUTTON = 21

logger = logging.getLogger()
printer = Adafruit_Thermal(SERIAL_PORT, PRINTER_BAUD_RATE, timeout=5)

# Init GPIO states
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_BUTTON, GPIO.OUT)
GPIO.setup(PRINT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init():
  print('Running xword-printer...')

  while True:
    button_state = GPIO.input(PRINT_BUTTON)

    if button_state == False:
      print("\nThe Button has been pressed.\n")
      GPIO.output(LED_BUTTON, GPIO.HIGH)

      fetch_xword()
      date, clues = load_date_clues(PUZZLE_TEXT_PATH)
      print_header(date)
      print_xword(clues)

      GPIO.output(LED_BUTTON, GPIO.LOW)
      end()

    else:
      GPIO.output(LED_BUTTON, GPIO.LOW)

def fetch_xword():
  print('Running xword-fetcher...')

  # Run node script as subprocess and stream output live
  npm_run_cmd = ["npm", "run", "start"]
  with Popen(npm_run_cmd, stdout=PIPE, text=True, bufsize=1) as p:
    for line in p.stdout:
      print(line, end='')

def load_date_clues(fName):
  print(f'* Loading text from: {PUZZLE_TEXT_PATH}...')

  try:
    f = open(fName)
    date = f.readline().rstrip('\n')
    next(f)
    clues = f.read()
    f.close()
    print(f'* Retrieved date: {date}')
    return date, clues
  except:

    print(f'{PUZZLE_TEXT_PATH} not found', file=sys.stderr)

def print_header(date):
  print('* Printing header text...')

  printer.justify('C')
  printer.setSize('M')
  printer.printImage(LOGO_PATH)
  printer.println('The New York Times')
  printer.println('Daily Mini Crossword')
  printer.setSize('S')
  printer.boldOn()
  printer.println(date)
  printer.boldOff()

def print_xword(clues):
  printer.justify('L')
  printer.feed(1)

  print(f'* Printing board image from: {BOARD_PATH}...')
  printer.printImage(BOARD_PATH)

  print(f'* Printing clues from: {PUZZLE_TEXT_PATH}...')
  printer.println(clues)
  printer.feed(4)
  print('')
  print('Happy puzzling!')

def end():
  printer.sleep()
  sys.exit()

init()