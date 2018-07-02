#!/usr/bin/env python3
# File    : hail.py - A simple caeser cipher with a key for the Automox Blog
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  07/01/2018 
# Copyright (C) 2018 Joe McManus

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import string
from  more_itertools import unique_everseen

parser = argparse.ArgumentParser(description='Caesar Cipher With Keyword')
parser.add_argument('keyword', help="Keyword or Phrase", type=str)
parser.add_argument('inputText', help="plaintext or ciphertext", type=str)
parser.add_argument('--encrypt', help="Encrypt phrase", action="store_true")
parser.add_argument('--decrypt', help="Decrypt phrase", action="store_true")
args=parser.parse_args()


#cleanup keyword and input
def cleanup(x):
    x=x.lower()
    x=x.replace(' ', '')
    return x

def plainAlpha():
    letters=[]
    for letter in string.ascii_lowercase:
        letters.append(letter)
    return letters

def createCipherAlpha(unique):
    i=len(unique)
    cipherAlpha=unique[:]
    for letter in plainAlpha():
        if letter not in unique:
            cipherAlpha.append(letter)
            i+=1
        if i == 26:
            break
    return cipherAlpha
    
def createMap(key, value):
     #Create a way to map plain words to cipherAlpha
     lookupTable=dict(zip(key,value))
     return lookupTable

def createMessage(inputText, lookupTable):
    cipherText=""
    for letter in inputText:
        cipherText=cipherText + lookupTable[letter]
    return cipherText

#remove spaces and shift to lower from user input
inputText=cleanup(args.inputText)
keyword=cleanup(args.keyword)

#Get a unique list of letters preserving order from the keyword
unique=list(unique_everseen(keyword))
#Create a cipher alphabet using the unique letters
cipherAlpha=createCipherAlpha(unique)

if args.encrypt:
    #Create a way to map plain words to cipherAlpha
    lookupTable=createMap(cipherAlpha, plainAlpha())

if args.decrypt:
    #Build an cipherAlphabet using the keyword
    lookupTable=createMap(plainAlpha(),cipherAlpha)

cipherText=createMessage(inputText, lookupTable)
print("Keyword:{}  \nUnique: {}\nOffset: {}\nOutput: {}\n".format(keyword, unique, len(unique), cipherText))
