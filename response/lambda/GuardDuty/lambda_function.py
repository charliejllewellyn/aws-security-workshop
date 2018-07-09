import boto3
import time

ec2Client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def getResource(event):

    return event['detail']['resource']['instanceDetails']['instanceId']

def snapShotInstance(instanceId):

    response = ec2Client.describe_instance_attribute(
    Attribute='blockDeviceMapping',
    InstanceId=instanceId
    )
    volumeId = response['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    snapshot = ec2.create_snapshot(VolumeId=volumeId, Description='Security Workshop Example')
    snapshot.load()
    while snapshot.state != 'completed':
        print(snapshot.progress)
        print("Snapshot under creation")
        time.sleep(10)
        snapshot.load()
    else:
        print("snapshot READY")
        return snapshot

def terminateInstance(instanceId):
    response = ec2Client.terminate_instances(
    InstanceIds=[ instanceId ]
    )

def lambda_handler(event, context):
    instanceId = getResource(event)
    snapShotInstance(instanceId)
    terminateInstance(instanceId)
