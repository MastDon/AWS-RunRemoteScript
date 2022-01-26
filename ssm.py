import time
import json
import boto3

# boto3 client
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
sns = boto3.client('sns', region_name="eu-central-1")

# getting instance information
describeInstance = ec2.describe_instances()

InstanceId = []

# fetching public ip address of the running instances

for i in describeInstance['Reservations']:
    for instance in i['Instances']:
        if instance["State"]["Name"] == "running":
            InstanceId.append(instance['InstanceId'])

    # print(InstanceId['InstanceId'])

for instanceid in InstanceId:
    response = ssm.send_command(
        InstanceIds=[instanceid],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [
            'zip -r /tmp/mi/$(hostname)_`date +%Y%m%d_%H:%M:%S`.zip /tmp && aws s3 cp /tmp/mi s3://dp-s3-education/backup_test/ --recursive']}, )
    command_id = response['Command']['CommandId']

    time.sleep(3)

    output = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId=instanceid
    )

    print(output)

sns.publish(
    TopicArn='arn:aws:sns:eu-central-1:055524789533:Lambda-Notification',
    Subject='EC2 files backup',
    Message='Successful create files backup for instances : ' + str(InstanceId),

)
