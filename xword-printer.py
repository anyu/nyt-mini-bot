#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
import os, time, logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

LOGO_FILE = "nyt-logo.png"
IMAGE_FILE = "puzzle.png"
CLUES_FILE = "clues.txt"

def printHeader():
  logger.info('Printing header text...')

  printer.justify('C')
  printer.setSize('M')
  printer.printImage(LOGO_FILE)
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
  printer.printImage(IMAGE_FILE) 
  printer.println(clues)
  printer.feed(3)

printHeader()
clues = loadClues(CLUES_FILE)
printXwordWithClues()

printer.sleep()