import webbrowser
import dynamodb
import doGPS
import boto3
import folium
from boto3.dynamodb.conditions import Key

def displayAllNodeMeasurements(region,bssid,ssid):
  db=dynamodb.query(region)
  result=db.getMeasurementsById(bssid,ssid)
  return result
#  measurements=[]
#  for measurement in results:
#    measurements.append(["GPS"])
#  map_ = folium.Map(location=[30.45,-84.32], zoom_start=10)
#  for measurement in range(0,len(measurements)):
#    folium.Marker(arr[q]).add_to(map_)
#  map_.save("/home/pi/visuals/PrettyFlyforaWi-fi.html")

def displayAllNodesFrom(region,attribute_list):
  db=dynamodb.query(region)
  nodes=db.queryTableForAttributes(attribute_list)
  map_ = folium.Map(location=[30.45,-84.32], zoom_start=10)
  for node in nodes["Items"]:
    # move repetive code
    try:
      html=generateNodeHTML(node)
      folium.Marker(node["Minimum"]["GPS"],popup=html).add_to(map_)
    except KeyError:
      pass
  map_.save("/home/pi/googlemapped/visuals/prototype_result3.html")

#call this function to filter an attribute y with value x
#for example displayAllNodesInculding("Vendor", "NETGEAR","30.45,-84.32")
def displayAllNodesInculding(region,attribute,value):
  db=dynamodb.query(region)
  nodes=db.queryTableWithFilter(attribute,value)
  map_ = folium.Map(location=[30.45,-84.32], zoom_start=10)
  for node in nodes:
    # move repetive code into generateNodeHTML
    try:
      html=generateNodeHTML(node)
      folium.Marker(node["Minimum"]["GPS"],popup=html).add_to(map_)
    except KeyError:
      pass
  map_.save("/home/pi/googlemapped/visuals/testingtesting123.html")

def generateNodeHTML(node):
  node_indenity="<b>"+node["BSSID"]+"<br>"+node["SSID"]+"<br>"
  node_information=node["Vendor"]+"<br>"+node["Minimum"]["RSSI"]+"<br>"+str(node["Minimum"]["GPS"])
  html=node_indenity+node_information
  return html

#def displayAllNodesExculding(region,attribute,value):
#make a scan for everything but

#def generateAtrributeStatistics(region):
#get attributes method in scan for dynamodb resourses

#get the name of every vendor within a region

allofem=[]
for j in x["Items"]:
  allofem.append(j["Vendor"])

for test in arr:
  print (test)
  print ("Percentage of occurance in this region: ",allofem.count(test)/len(allofem)*100)


