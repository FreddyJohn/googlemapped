import os
import re
import json
import time
import doGPS
import random
import serial
import datetime
import subprocess
from subprocess import Popen, PIPE
from mac_vendor_lookup import MacLookup
os.system('mkdir /tmp/uploads')
while True:
  os.system('sudo find /tmp/uploads -type f -cmin +5 -delete')
  command=r"""sudo iw dev wlan0 scan |
           egrep 'signal:|SSID:|^BSS' |
           sed -e 's/\tsignal: //' -e 's/\tSSID: //' -e 's/\tBSS: //' |
           awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' |
           sort """
  time_stamp=str(datetime.datetime.now())
  results=str(subprocess.check_output(command,shell=True).decode('utf-8')).split('BSS',-1)
  nodes={}
  measurement={}
  position=doGPS.getPosition()
  latlng_block=doGPS.getTableNameFrom(position)
  nodes["Region"]=latlng_block
  for node in results:
    if len(node)>0 and node.find('associated')==-1:
      node=node.replace('(on wlan0)','')
      node=node.replace('BSS','')
      node=node.replace('dBm', '').strip()
      mac=node.split()[0]
      ssid=node[node.find(node.split()[1])+len(node.split()[1])+2:len(node)]
      rssi=node.split()[1]
      node=node.split()
      if ssid=='':
        nodes["SSID"]=mac
      else:
        nodes["SSID"]=ssid
      nodes["BSSID"]=mac
      measurement["RSSI"]=rssi
      measurement["Date"]=time_stamp
      measurement["GPS"]=position
      nodes["Measurements"]=[measurement]
      try:
        raw=MacLookup().lookup(mac)
        vendor=re.sub('[^A-Za-z0-9]+', '',raw)
        nodes["Vendor"]=vendor.replace(" ", "")
      except KeyError:
        nodes["Vendor"]="UnknownVendor"
      print (nodes)
      newname=str(time.time()).replace('.',str(random.randint(256,1024)))
      filename='/tmp/uploads/temp_Id'+newname+'.txt'
      with open(filename,'w') as out:
        json.dump(nodes,out)
      process=Popen(['python3','autodb.py',filename])
