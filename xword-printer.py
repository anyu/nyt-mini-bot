#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
import os, sys, logging, subprocess
import RPi.GPIO as GPIO

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

LOGO_PATH = "images/nyt-logo.png"
BOARD_PATH = "xwdBoard.png"
PUZZLE_TEXT_PATH = "puzzle.txt"

# GPIO PINS (BCM numbers)
LED_BUTTON = 20
PRINT_BUTTON = 21

# Init GPIO states
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_BUTTON, GPIO.OUT)
GPIO.setup(PRINT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def fetchXword():
  try:
    # nvmCmd = "nvm use v14.4.0"
    # nvmCmdResult = subprocess.run(["/bin/bash", "-i", "-c", nvmCmd], capture_output=True,text=True)
    # print(nvmCmdResult.stdout)
    # logger.error(nvmCmdResult.stderr)

    print('Running xword-fetcher...')
    npmRunCmd = ["npm", "run", "start"]
    npmRunCmdResult = subprocess.run(npmRunCmd, capture_output=True, text=True)
    print(npmRunCmdResult.stdout)
    logger.error(npmRunCmdResult.stderr)
  except:
    print('Error running xword-fetcher', file=sys.stderr)

def loadDateAndClues(fName):
  print(f'Loading text from: {PUZZLE_TEXT_PATH}...')

  try:
    f = open(fName)
    date = f.readline().rstrip('\n')
    next(f)
    clues = f.read()
    f.close()
    print(f'Retrieved date: {date}')
    return date, clues
  except:

    print(f'{PUZZLE_TEXT_PATH} not found', file=sys.stderr)

def printHeader(date):
  print('Printing header text...')

  printer.justify('C')
  printer.setSize('M')
  printer.printImage(LOGO_PATH)
  printer.println('The New York Times')
  printer.println('Daily Mini Crossword')
  printer.setSize('S')
  printer.boldOn()
  printer.println(date)
  printer.boldOff()

def printXword(clues):
  printer.justify('L')
  printer.feed(1)

  print(f'Printing board image from: {BOARD_PATH}...')
  printer.printImage(BOARD_PATH)

  print(f'Printing clues from: {PUZZLE_TEXT_PATH}...')
  printer.println(clues)
  printer.feed(4)
  print('')
  print('Happy puzzling!')

def init():
  fetchXword()
  date, clues = loadDateAndClues(PUZZLE_TEXT_PATH)
  printHeader(date)
  printXword(clues)
  end()

def end():
  printer.sleep()
  sys.exit()

while True:
  button_state = GPIO.input(PRINT_BUTTON)

  if button_state == False:
    print("The Button has been pressed.\n")
    GPIO.output(LED_BUTTON, GPIO.HIGH)
    init()
    GPIO.output(LED_BUTTON, GPIO.LOW)

  else:
    GPIO.output(LED_BUTTON, GPIO.LOW)
