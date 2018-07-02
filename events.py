#!/usr/bin/env python3
#File: events.py : An example script using the Automox API 
#Auth: Joe McManus mcmanus@automox.com
#Ver : Version 1.0 2018/06/12 

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
import shutil
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Automox API Example')
parser.add_argument('--limit', help="Limit results to X", type=int)
parser.add_argument('--csv', help="Output as CSV",  action="store_true")
parser.add_argument('--table', help="Output as table",  action="store_true")
parser.add_argument('--errors', help="Show errors only",  action="store_true")
parser.add_argument('apiKey', help="API Key ", type=str)
args=parser.parse_args()


def formatCell(x):
    x.rstrip("\r\n")
    #make sizeable for screen
    termWidth=shutil.get_terminal_size().columns
    #Assume half the screen for error messages
    colWidth= round(termWidth /2)
    chunks=""
    if len(x) > colWidth:
        for chunk in [x[i:i+colWidth] for i in range(0, len(x), colWidth)]:
            if len(chunk) == colWidth:
                chunks += chunk + "\n"
            else:
                chunks += chunk
        return chunks
    else:
        return x

baseUrl="https://console.automox.com/api/events?api_key="
url=baseUrl + args.apiKey 

i=0
pageText=requests.get(url).json()

if args.csv: 
    filename=datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "-events.csv"
    fh=open(filename, "w+") 

table=PrettyTable(["Date", "Host", "Error"])
table.align["Error"] = "l"
for event in pageText:
    if 'data' in event:
        if 'status' in event['data']:
            if event['data']['status'] != 0:
                if args.table:
                    table.add_row([event['create_time'].split('+')[0], event['server_name'], formatCell(event['data']['text'])])
                if args.csv: 
                    csvRow = event['create_time'].split('+')[0] + "," + event['server_name'] + "," + event['data']['text']
                    fh.write(str(csvRow))

            if args.limit:
                if i >= args.limit:
                    break
                i+=1

if args.table:
    print(table)
if args.csv:
    fh.close()

