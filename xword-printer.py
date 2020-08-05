#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
import os, sys, time, logging, subprocess

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

LOGO_PATH = "images/nyt-logo.png"
BOARD_PATH = "xwdBoard.png"
PUZZLE_TEXT_PATH = "puzzle.txt"

def fetchXword():
  try:
    # nvmCmd = "nvm use v14.4.0"
    # nvmCmdResult = subprocess.run(["/bin/bash", "-i", "-c", nvmCmd], capture_output=True,text=True)
    # print(nvmCmdResult.stdout)
    # logger.error(nvmCmdResult.stderr)

    npmRunCmd = ["npm", "run", "start"]
    npmRunCmdResult = subprocess.run(npmRunCmd, capture_output=True, text=True)
    print(npmRunCmdResult.stdout)
    logger.error(npmRunCmdResult.stderr)
  except:
    print('Error running node xword fetcher script', file=sys.stderr)

def printHeader():
  print('Printing header text...')

  printer.justify('C')
  printer.setSize('M')
  printer.printImage(LOGO_PATH)
  printer.println('The New York Times')
  printer.println('Daily Mini Crossword')
  printer.setSize('S')
  printer.boldOn()
  printer.println(time.strftime('%A, %b %d, %Y'))
  printer.boldOff()

def loadClues(fName):
  print(f'Loading clues from: {PUZZLE_TEXT_PATH}...')

  try:
    f = open(fName)
    result = f.read()
    f.close()
    return result
  except:
    print(f'{PUZZLE_TEXT_PATH} not found', file=sys.stderr)

def printXword():
  printer.justify('L')
  printer.feed(1)

  print(f'Printing board image from: {BOARD_PATH}...')
  printer.printImage(BOARD_PATH)

  print(f'Printing clues from: {PUZZLE_TEXT_PATH}...')
  printer.println(clues)
  printer.feed(4)

fetchXword()
printHeader()
clues = loadClues(PUZZLE_TEXT_PATH)
printXword()

printer.sleep()
