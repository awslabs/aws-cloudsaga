#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate attacks in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS


import logging
import boto3
import datetime
from datetime import timezone


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


sts = boto3.client('sts')


region_list = ['af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'eu-south-1', 'me-south-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
region_list_no_opt_in = ['ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']


# Network Changes
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


# Step 2. Attempt to create a VPC in regions where no current instances exist (DryRun).
def suspicious_vpc_calls(regions_containing_instances):
    """Function to call VPC APIs that are suspicious"""
    working_list = (list(set(region_list_no_opt_in) - set(regions_containing_instances)))
    for aws_region in working_list:
        try:
            ec2_unused = boto3.client('ec2', region_name=aws_region)
            logging.info("Creating rogue Amazon VPC in region " + aws_region + "...")
            logging.info("CreateVpc API Call")
            ec2_unused.create_vpc(
                CidrBlock='192.168.220.0/24',
                DryRun=True,
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'CS-Purpose',
                                'Value': 'c-level-mine'
                            },
                        ]
                    }
                ]
            )
        except Exception as exception_handle:
            logging.error(exception_handle)


# Step 3. Attempt to create Security Groups in regions that contain instances (DryRun).
def create_security_groups(regions_containing_instances):
    """Function to create Security Groups in regions that contain instances"""
    for aws_used_region in regions_containing_instances:
        try:
            VPCList: list = []
            vpcs_in_use = boto3.client('ec2', region_name=aws_used_region)
            logging.info("Looking for existing VPCs to run DryRun attacks in region " + aws_used_region + "...")
            logging.info("DescribeVpcs API Call")
            all_vpcs = vpcs_in_use.describe_vpcs()
            for vpc_id in all_vpcs["Vpcs"]:
                VPCList.append(vpc_id["VpcId"])
            for vpc_create_sg in VPCList:
                logging.info("Creating Security Group in existing VPC (DryRun)...")
                sg_create = vpcs_in_use.create_security_group(
                    Description="open-2-everyone",
                    GroupName='open-2-everyone',
                    VpcId=vpc_create_sg,
                    DryRun=True,
                    TagSpecifications=[
                        {   
                            'ResourceType': 'security-group',
                            'Tags': [
                                {
                                    'Key': 'CS-Purpose',
                                    'Value': 'public-access-for-all'
                                }
                            ]
                        }
                    ]
                )
        except Exception as exception_handle:
            logging.error(exception_handle)


def main():
    """Function that runs all of the previously defined functions"""
    regions_containing_instances = list_region_containing_instances()
    suspicious_vpc_calls(regions_containing_instances)
    create_security_groups(regions_containing_instances)
    logging.info("This is the end of the script. Please check and cleanup any resources created from this script.")