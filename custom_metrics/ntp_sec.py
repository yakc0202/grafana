import os
import boto3
import datetime
def put_custom_metric(value, dimensions):
    cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
    response = cloudwatch.put_metric_data(
        Namespace='ntpd_sync',
        MetricData=[
            {
                'MetricName': 'ntp_sync',
                'Dimensions': dimensions,
                'Timestamp': datetime.datetime.utcnow(),
                'Value': value,
                'Unit': 'Seconds'
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

def check_ntp():
    try:
        arr = os.popen('chronyc tracking | grep System').read().split(':')[1].split(' ')
        hostname = 'grafana-update-ntp'
        sec = float(arr[1])
        word = arr[3]

        if word == 'fast':
            dimensions[0].update({'Value':hostname})
            put_custom_metric(sec, dimensions)
            print(f"{hostname} is {sec}")
        elif word == 'slow':
            dimensions[0].update({'Value':hostname})
            put_custom_metric(-sec, dimensions)
            print(f"{hostname} is {-sec}")

    except:
        raise

if __name__ == '__main__':
    check_ntp()
