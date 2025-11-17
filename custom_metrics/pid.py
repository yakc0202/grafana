import os
import boto3
import datetime
import sys

def put_custom_metric(value, dimensions):
    cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
    response = cloudwatch.put_metric_data(
        Namespace='PID',
        MetricData=[
            {
                'MetricName': 'pidcheck',
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


def check_pid(name):
    try:
        #name = 'apache'
        cnt = int(os.popen('ps -ef | grep ^'+name+' | wc -l').read())
        dimensions[0].update({'Value':name})
        put_custom_metric(cnt, dimensions)
        print(f"{name} is {cnt}")
    except Exception as e:
        dimensions[0].update({'Value':name})
        put_custom_metric(0, dimensions)
        print(f'{name} is 0')


if __name__ == '__main__':
#    check_pid()
    if len(sys.argv) > 1:
        name = sys.argv[1]
        check_pid(name)
