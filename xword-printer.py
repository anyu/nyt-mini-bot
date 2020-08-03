#!/usr/bin/python3

from Adafruit_Thermal import *
from PIL import Image
import os, time

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

IMAGE_FILE = "puzzle.png"
CLUES_FILE = "clues.txt"

def loadClues(fName):
  f = open(fName)
  result = f.read()
  f.close()
  return result

def printHeader():
  printer.justify('C')
  printer.setSize('M')
  printer.println('The New York Times')
  printer.println('Daily Mini Crossword')
  printer.setSize('S')
  printer.boldOn()
  printer.println(time.strftime('%A, %b %d, %Y'))
  printer.boldOff()

def printXwordWithClues():
  printer.justify('L')
  printer.feed(1)
  printer.printImage(IMAGE_FILE) 
  printer.println(clues)
  printer.feed(3)

clues = loadClues(CLUES_FILE)
printHeader()
printXwordWithClues()

printer.sleep()