import webbrowser
import dynamodb
import doGPS
import boto3
import folium
from boto3.dynamodb.conditions import Key

dynamodb_resource = boto3.resource('dynamodb')
def test_add_attribute():
  db_write=dynamodb.dynamo_write("30.45_-84.32","2c:30:33:64:be:0f","NETGEAR09")
  x={'RSSI': '-87.00', 'Date': '2020-08-30 12:43:36.632121', 'GPS': ['30.451656166666666', '-84.32470433333333']}
  db_write.createItemAttribute(x)

def test_min_function():
  db_read=dynamodb.dynamo("30.45_-84.32","2c:30:33:64:be:0f","NETGEAR09")
  meas=db_read.getMeasurementsById()
  best=db_read.getBestSingalFromMeasurements(meas)
  return best

def test_gps_module():
  test=doGPS.getPosition()
  test1=doGPS.getTableNameFrom(test)
  print (test,test1)

def test_get_measurements():
  test=dynamodb.dynamo("30.45_-84.32","90:72:40:27:11:c5","Pretty Fly for a Wi-fi")
  result=test.getMeasurementsById()
  return result

def prototype_visualization(arr):
  map_ = folium.Map(location=[30.45,-84.32], zoom_start=10)
  for q in range(0,len(arr)):
    folium.Marker(arr[q]).add_to(map_)
  map_.save("PrettyFlyforaWi-fi.html")

#client=boto3.client("dynamodb")
#response=client.scan(TableName="30.45_-84.32",ScanFilter={"Vendor":{"AttributeValueList": [{'S': 'PEGATRONCORPORATION'}],"ComparisonOperator":'BEGINS_WITH'}})
def prototype_get_WAP_positions_from_db():
   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('30.45_-84.32')
   response = table.scan(AttributesToGet=['Minimum'])
   return response
"""
x=prototype_get_WAP_positions_from_db(()
arr=[]
for y in x['Items']:
	try:
		arr.append(y['Minimum']['GPS'])
	except KeyError:
		print ("Not enough measurements for this Node")
print (arr)
prototype_visualization(arr)
"""

"""
x=test_get_measurements()
meas=[]
for y in x:
	meas.append(y["GPS"])
print(meas)
prototype_visualization(meas)
"""
#test_min_function()


def scan_table_allpages(table_name, filter_key=None, filter_value=None):
    table = dynamodb_resource.Table(table_name)

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items

#test=scan_table_allpages("30.45_-84.32","Vendor","PEGATRONCORPORATION")

table = dynamodb_resource.Table("30.45_-84.32")
x = table.scan(AttributesToGet=['Minimum',"BSSID","SSID","Vendor"])
map_ = folium.Map(location=[30.45,-84.32], zoom_start=10)
for y in x["Items"]:
  try:
    node_indenity="<b>"+y["BSSID"]+"<br>"+y["SSID"]+"<br>"
    node_information=y["Vendor"]+"<br>"+y["Minimum"]["RSSI"]+"<br>"+str(y["Minimum"]["GPS"])+"<b>"
    html=node_indenity+node_information
    print (html)
    folium.Marker(y["Minimum"]["GPS"],popup=html).add_to(map_)
  except KeyError:
    print("no gps data")

map_.save("prototype_result3.html")


#THOUGHTS
#functionality to delete measurements older than x and truncate a measurement within a list of measurements over a certain value
