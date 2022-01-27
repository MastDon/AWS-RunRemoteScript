import time
import json
import boto3

# boto3 client
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

# getting instance information
describeInstance = ec2.describe_instances()

InstanceId = []

# fetching public ip address of the running instances

for i in describeInstance['Reservations']:
    for instance in i['Instances']:
        if instance["State"]["Name"] == "running":
            InstanceId.append(instance['InstanceId'])

     print(InstanceId['InstanceId'])
