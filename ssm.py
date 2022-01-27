import boto3
import time
import datetime

ec2 = boto3.resource('ec2')

sns = boto3.client('sns', region_name="eu-central-1")

backup_filter = [
    {
        'Name': 'tag:Backup',
        'Values': ['Yes']

    }

]

ami_ids = []

for ins in ec2.instances.filter(Filters=backup_filter):
    ins.create_image(
        Name='dev-pro-demo-ami' + str(time.time()),
        Description='Set your description here ',
        NoReboot=True

    ),
    ami_ids.append(ins.instance_id),

    sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:055524789533:Lambda-Notification',
        Subject='EC2 backup AMI',
        Message='Successful create AMI for instances : ' + str(ami_ids),

    )

