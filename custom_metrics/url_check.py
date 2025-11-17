import boto3
import datetime
import requests
from time import sleep

def put_custom_metric(value, dimensions):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.put_metric_data(
        Namespace='HttpReturnCode',
        MetricData=[
            {
                'MetricName': 'httpStatuCode',
                'Dimensions': dimensions,
                'Timestamp': datetime.datetime.utcnow(),
                'Value': value,
                'Unit': 'Count'
            },
        ]
    )
    return response

dimensions = [
    {
        'Name': 'Name',
        'Value': ''
    },
]

with open('urlList.txt', 'r') as url:
    url = url.readlines()

try:
    for x in url:
        try:
            checkList = x.split()
            sleep(2)
            response = requests.get(checkList[1])
            httpStatuCode = response.status_code
#           dimensions[0].update({'Value':checkList[0]})
#           put_custom_metric(httpStatuCode, dimensions)
            print('{} : {}'.format(checkList[0], httpStatuCode))
        except requests.RequestException as e:
#           dimensions[0].update({'Value':checkList[0]})
#           put_custom_metric(0, dimensions)
            print(checkList[0], ':' ,0)
            #print(e)
except requests.RequestException as e:
    pass
#    dimensions[0].update({'Value':checkList[0]})
#    put_custom_metric(0, dimensions)
    #print(checkList[0], ':' ,0)