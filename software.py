#!/usr/bin/env python3
#File: noncomp.py : A script to get missing software patches from Automox API
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
parser.add_argument('--graph', help="Output as table",  action="store_true")
parser.add_argument('--dump', help="Just dump the data and exit, useful for troubleshooting",  action="store_true")
parser.add_argument('apiKey', help="API Key ", type=str)
parser.add_argument('orgId', help="AMX Org ID ", type=str)
args=parser.parse_args()


baseUrl="https://console.automox.com/api/software_version?api_key="
url=baseUrl + args.apiKey  + "&o=" + args.orgId + "&pendingUpdate=1"

i=0
pageText=requests.get(url).json()


if args.graph:
    try:
        import plotly
        import plotly.graph_objs as go
        xData=[]
        yData=[]
    except:
        print("ERROR: Plotly not installed, try pip3 install plotly") 
        quit()

if args.dump:
    print(pageText)
    for item in pageText['results']:
        serverName=item['display_name']
        for item2 in item['pending_update']:
            missingCount=item2['server_count']
        print( serverName + " " + str(missingCount))
    quit()

if args.csv: 
    filename=datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "-noncomp.csv"
    fh=open(filename, "w+") 

table=PrettyTable(["Package",  "Machines to be Upgraded"])
for item in pageText['results']:
    packageName=item['display_name']
    for item2 in item['pending_update']:
        missingCount=item2['server_count']
    if args.table:
        table.add_row([packageName, missingCount])
    if args.csv: 
        fh.write("\"{}\" , {}".format(packageName, missingCount))
    if args.graph:
            xData.append(packageName)
            yData.append(missingCount)

    if args.limit:
        if i >= args.limit:
            break
    i+=1

if args.table:
    print(table)
if args.csv:
    fh.close()
if args.graph:
    plotly.offline.plot({ 
         "data":[plotly.graph_objs.Bar(x=xData, y=yData)],
         "layout":plotly.graph_objs.Layout(title="Missing Package Count",
             xaxis=dict(title="Package Name"),
             yaxis=dict(title="Count"))})
