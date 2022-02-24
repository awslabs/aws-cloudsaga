#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate security events in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS


import logging
import boto3
import datetime
from botocore.exceptions import ClientError, InvalidS3AddressingStyleError
from datetime import timezone


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


sts = boto3.client('sts')


region_list = ['af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'eu-south-1', 'me-south-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
region_list_no_opt_in = ['ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']


# List of AMIs used within the Bitcoin Miner/EC2 Forensics Standup code
ec2_ami = {
    'ap-south-1': 'ami-04bde106886a53080',
    'ap-northeast-1': 'ami-0fe22bffdec36361c',
    'ap-northeast-2': 'ami-0ba5cd124d7a79612',
    'ap-northeast-3': 'ami-092faff259afb9a26',
    'ap-southeast-1': 'ami-055147723b7bca09a',
    'ap-southeast-2': 'ami-0f39d06d145e9bb63',
    'ca-central-1': 'ami-0e28822503eeedddc',
    'eu-central-1': 'ami-0b1deee75235aa4bb',
    'eu-west-1': 'ami-0943382e114f188e8',
    'eu-west-2': 'ami-09a56048b08f94cdf',
    'eu-west-3': 'ami-06602da18c878f98d',
    'eu-north-1': 'ami-0afad43e7d620260c',
    'sa-east-1': 'ami-05aa753c043f1dcd3',
    'us-east-1': 'ami-0747bdcabd34c712a',
    'us-east-2': 'ami-00399ec92321828f5',
    'us-west-1': 'ami-07b068f843ec78e72',
    'us-west-2': 'ami-090717c950a5c34d3'
}


# EC2 Forensics/Bitcoin Miners
# Step 1. Find regions without instances.
def list_region_containing_instances():
    """Function to find regions containing ec2 instances and store them in a list"""
    regions_containing_instances=[]
    for aws_region in region_list_no_opt_in:
        ec2=boto3.client('ec2',region_name=aws_region)
        logging.info("Checking region " + aws_region + " for existing EC2 Instances...")
        logging.info("DescribeInstances API Call")
        instances = ec2.describe_instances()
        instance_ID=None
        for instance in instances['Reservations']:
            instance_ID=instance['Instances'][0]['InstanceId']
            if not (instance_ID == None):
                regions_containing_instances.append(aws_region)
    return regions_containing_instances


# Step 2. Attempt to create EC2 instances with high compute in unused regions (DryRun)
def ec2_create_instances_unused_region(regions_containing_instances):
    """Function to attempt creating high volume of instances in an unused region and make them public"""
    working_list = (list(set(region_list_no_opt_in) - set(regions_containing_instances)))
    for aws_region in working_list:
        try:
            region_image = ec2_ami[aws_region]
            ec2=boto3.client('ec2',region_name=aws_region)
            logging.info("Spinning up Bitcoin Miners (DryRun) in region " + aws_region + "...")
            logging.info('RunInstances API Call')
            instance=ec2.run_instances(
                ImageId=region_image,
                InstanceType='c5.24xlarge',
                MaxCount=2,
                MinCount=1,
                DryRun=True,
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-gpu',
                        'Tags': [
                            {
                                'Key': 'CS-Purpose',
                                'Value': 'c-level-mine'
                            },
                        ]
                    },
                ],
            )
        except Exception as exception_handle:
            logging.error(exception_handle)


def main():
    """Function that runs all of the previously defined functions"""
    regions_containing_instances = list_region_containing_instances()
    ec2_create_instances_unused_region(regions_containing_instances)
