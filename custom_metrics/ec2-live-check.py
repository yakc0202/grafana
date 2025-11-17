import boto3
import datetime

def put_custom_metric(value, dimensions):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.put_metric_data(
        Namespace='Ec2-Live-Check',
        MetricData=[
            {
                'MetricName': 'live-check',
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

sts = boto3.client('sts')
assume_role = sts.assume_role(RoleArn ='arn:aws:iam::186021893207:role/SHLW-AN2-FCM-EC2-CLOUDWATCH-ASSUME-ROLE',RoleSessionName = 'AssumeRoleSession')

ec2 = boto3.client('ec2',aws_access_key_id = assume_role['Credentials']['AccessKeyId'], aws_secret_access_key = assume_role['Credentials']['SecretAccessKey'],aws_session_token = assume_role['Credentials']['SessionToken'])

def get_instance_name_and_state(instance):
    instance_name = None
    instance_state = instance['State']['Name']
    
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            instance_name = tag['Value']
    
    return instance_name, instance_state

response = ec2.describe_instances()
instances_with_names_and_states = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_name, instance_state = get_instance_name_and_state(instance)
        if instance_name is not None:
            instances_with_names_and_states.append((instance_name, instance_state))

for name, state in instances_with_names_and_states:
    if state == "running":
        dimensions[0].update({'Value':name})
        put_custom_metric(0, dimensions)
        print(f"{name}, : {state}")
    else:
        dimensions[0].update({'Value':name})
        put_custom_metric(1, dimensions)
        print(f"{name}, : {state}")