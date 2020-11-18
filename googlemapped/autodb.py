import sys
import json
import dynamodb

def begin_upload_process(nodes):
    db=dynamodb.dynamo(nodes["Region"],nodes["BSSID"],nodes["SSID"])
    db.createNewTable()
    db.appendDataToItemAttribute(nodes)

    arr=db.getMeasurementsById()
    best_signal=db.getBestSingalFromMeasurements(arr)
    db.createItemAttribute(best_signal)

if __name__ == '__main__':
    data={}
    filename=str(sys.argv[1])
    with open(filename) as json_file:
        data=json.load(json_file)
    begin_upload_process(data)

