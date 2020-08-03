#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
import os, time, logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

LOGO_PATH = "nyt-logo.png"
XWORD_PATH = "puzzle.png"
CLUES_PATH = "clues.txt"

def printHeader():
  logger.info('Printing header text...')

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
  logger.info('Loading clues...')

  f = open(fName)
  result = f.read()
  f.close()
  return result

def printXwordWithClues():
  logger.info('Printing xword clues...')

  printer.justify('L')
  printer.feed(1)
  printer.printImage(XWORD_PATH)
  printer.println(clues)
  printer.feed(3)

printHeader()
clues = loadClues(CLUES_PATH)
printXwordWithClues()

printer.sleep()