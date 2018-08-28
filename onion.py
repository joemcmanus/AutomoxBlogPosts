#!/usr/bin/env python3
#File: onion.py : A script to get non compliant devices from the Automox API
#Auth: Joe McManus mcmanus@automox.com
#Ver : Version 1.0 2018/08/28 

import json
import requests
from prettytable import PrettyTable
import argparse
from datetime import datetime
import subprocess
import time

parser = argparse.ArgumentParser(description='Automox API Example')
parser.add_argument('--limit', help="Limit results to X", type=int)
parser.add_argument('--csv', help="Output as CSV",  action="store_true")
parser.add_argument('--table', help="Output as table",  action="store_true")
parser.add_argument('--lcd', help="Output on Onion LCD",  action="store_true")
parser.add_argument('--light', help="Output to light",  action="store_true")
parser.add_argument('apiKey', help="API Key ", type=str)
args=parser.parse_args()


baseUrl="https://console.automox.com/api/reports/noncompliance?api_key="
url=baseUrl + args.apiKey  + "&startDate=" + datetime.now().strftime('%Y-%m-%d')
print(url)

i=0
pageText=requests.get(url).json()

if args.csv: 
    filename=datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "-noncomp.csv"
    fh=open(filename, "w+") 

def writeLCD(msg):
	oledMsg="oled-exp -i -c write \"{}\"".format(msg)
	sendMsg=(subprocess.Popen(oledMsg, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()

def writeLight():
	lightCmd="relay-exp -i 0 1"
	sendLight=(subprocess.Popen(lightCmd, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()
	time.sleep(30)
	lightCmd="relay-exp -i 0 0"
	sendLight=(subprocess.Popen(lightCmd, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()
	

missingHosts=""
table=PrettyTable(["Host",  "OS", "Reboot Rqd", "packages"])
for item in pageText['nonCompliant']['devices']:
    missingPackages=None
    for item2 in item['policies']:
        for item3 in item2['packages']:
            if missingPackages == None:
                missingPackages=item3['name'] 
            else: 
                missingPackages= missingPackages + "\n" + item3['name']
    if args.table:
        table.add_row([item['name'], item['os_family'], item['needsReboot'], missingPackages])
    if args.csv: 
        fh.write("{} , {} , {}, \"{}\" ".format(item['name'], item['os_family'], item['needsReboot'], str(missingPackages).replace("\n", ",")))
    if args.lcd:
        missingHosts=missingHosts + " " + item['name']
    if args.limit:
        if i >= args.limit:
            break
    i+=1

if args.lcd:
    missingHosts=""
    i=0
    msg=("{} Hosts to be patched\n\nHosts: {}".format(i, missingHosts))
    if i == 0:
        msg="OK: No hosts missing patches" 
    writeLCD(msg)

if args.light:
    if i >= 5: 
        writeLight()

if args.table:
    print(table)
if args.csv:
    fh.close()

