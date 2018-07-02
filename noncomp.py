#!/usr/bin/env python3
#File: noncomp.py : A script to get non compliant devices from the Automox API
#Auth: Joe McManus mcmanus@automox.com
#Ver : Version 1.0 2018/06/19 
#
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

import json
import requests
from prettytable import PrettyTable
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Automox API Example')
parser.add_argument('--limit', help="Limit results to X", type=int)
parser.add_argument('--csv', help="Output as CSV",  action="store_true")
parser.add_argument('--table', help="Output as table",  action="store_true")
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

    if args.limit:
        if i >= args.limit:
            break
    i+=1

if args.table:
    print(table)
if args.csv:
    fh.close()

