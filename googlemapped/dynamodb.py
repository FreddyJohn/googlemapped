import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class build:

    def __init__(self,tablename, partitionkey, sortkey):
        self.dynamodb = boto3.resource('dynamodb')
        self.sortkey=sortkey
        self.tablename=tablename
        self.partitionkey=partitionkey
        self.table = self.dynamodb.Table(tablename)

    #LocalSecondaryIndexes < what are these how can they be useful?
    def createNewTable(self):
        dynamodb_client = boto3.client('dynamodb')
        #waiter = self.dynamodb.meta.client.get_waiter('table_exists')
        waiter = dynamodb_client.get_waiter('table_exists')
        try:
            table = self.dynamodb.create_table(
                TableName=self.tablename,
                KeySchema=[
                    {
                        'AttributeName': 'BSSID',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'SSID',
                        'KeyType': 'RANGE' # Sort Key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'BSSID',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'SSID',
                        'AttributeType': 'S'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            waiter.wait(
                TableName=self.tablename,
                WaiterConfig={
                    'Delay': 10,
                    'MaxAttempts': 123
                }
            )
        except dynamodb_client.exceptions.ResourceInUseException:
            pass

    def PopulateNewtable(self,data):
        print ("I am in the lat lng block: ", data["Region"])
        self.table.put_item(Item=data)

    def appendDataToItemAttribute(self,data):
        try:
            response = self.table.update_item(
                Key={
                    'BSSID': self.partitionkey,
                    'SSID': self.sortkey,
                    },
                UpdateExpression="set Measurements=list_append(Measurements,:r)", #=:r",
                ExpressionAttributeValues={
                    ':r': data["Measurements"],
                },
                ReturnValues="UPDATED_NEW"
            )
            return response
        except ClientError as E:
            self.PopulateNewtable(data)

    def createItemAttribute(self,data):
    #expression = "set "+attributename+" = :r"
        response = self.table.update_item(
            Key={
                'BSSID': self.partitionkey,
                'SSID': self.sortkey
                },
            UpdateExpression="set Minimum = :r",
            ExpressionAttributeValues={
                ':r': data,
            },
            ReturnValues="UPDATED_NEW"
        )
    # fix me thinkings
    def getMeasurementsById(self):
        try:
            response = self.table.get_item(Key={'BSSID': self.partitionkey, 'SSID': self.sortkey})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']['Measurements']

    def getBestSingalFromMeasurements(self,measurements):
        index=0
        best_signal={}
        global_min=None
        for measurement in measurements:
            if index<=len(measurements)-2:
                index+=1
                if global_min is None:
                    global_min=float(measurement["RSSI"])
                if global_min<float(measurements[index]["RSSI"]):
                    global_min=float(measurements[index]["RSSI"])
                    best_signal=measurements[index]
        return best_signal

class query:

    def __init__(self,table_name):
            dynamodb_resource = boto3.resource('dynamodb')
            self.table = dynamodb_resource.Table(table_name)

    def queryTableWithFilter(self, filter_key=None, filter_value=None):
        if filter_key and filter_value:
            filtering_exp = Key(filter_key).eq(filter_value)
            response = self.table.scan(FilterExpression=filtering_exp)
        else:
            response = self.table.scan()
        items = response['Items']
        while True:
            if response.get('LastEvaluatedKey'):
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items += response['Items']
            else:
                break
        return items

    def queryTableForAttributes(self,attribute_list):
         response = self.table.scan(AttributesToGet=attribute_list)
         return response["Items"]

    def getMeasurementsById(self,partitionkey,sortkey):
        try:
            response = self.table.get_item(Key={'BSSID': self.partitionkey, 'SSID': self.sortkey})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']['Measurements']

    def getBestSingalFromMeasurements(self,measurements):
        index=0
        best_signal={}
        global_min=None
        for measurement in measurements:
            if index<=len(measurements)-2:
                index+=1
                if global_min is None:
                    global_min=float(measurement["RSSI"])
                if global_min<float(measurements[index]["RSSI"]):
                    global_min=float(measurements[index]["RSSI"])
                    best_signal=measurements[index]
        return best_signal

    def getAllUniqueAttributeValues(self,attribute):
        uniquevalues=[]
        nodes = self.table.scan(AttributesToGet=[attribute])
        for node in nodes["Items"]:
            uniquevalues.append(node[attribute])
            occurrences=uniquevalues.count(node[attribute])
            if occurrences>=2:
                for delete in range(1,occurrences):
                    uniquevalues.remove(node[attribute])
        return uniquevalues


