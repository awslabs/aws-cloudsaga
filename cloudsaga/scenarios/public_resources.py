#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate security events in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS


import logging
import boto3
import datetime
import string
import random
import os
from botocore.exceptions import ClientError, InvalidS3AddressingStyleError
from datetime import timezone


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


sts = boto3.client('sts')
region = os.environ.get('AWS_REGION', 'us-east-1')


region_list = ['af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'eu-south-1', 'me-south-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
region_list_no_opt_in = ['ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
public_db_list: list = []


# Generating random password for RDS Database
def random_pass():
    """Function to create random RDS database password"""
    try:
        letters = string.ascii_letters
        numbers = string.digits
        special_chars = string.punctuation

        dummy_phrase = (''.join(random.choice(letters + numbers + special_chars) for char in range(24)))
        dummy_string = dummy_phrase.replace('@','').replace('/','').replace('"','')
    except Exception as exception_handle:
        logging.error(exception_handle)
    return(dummy_string)


# Define random string for S3 Bucket Name
def random_string_generator():
    lower_letters = string.ascii_lowercase
    numbers = string.digits
    unique_end = (''.join(random.choice(lower_letters + numbers) for char in range(6)))
    return unique_end


# Public Resources
# Step 1. Check for public RDS resources, and attempt to create & delete a public RDS database.
def public_resource_check(region_list, dummy_string):
    """Function to check for public resources"""
    for aws_region in region_list:
        try:
            logging.info("Checking RDS Instances in " + aws_region)
            rds = boto3.client('rds', region_name=aws_region)
            logging.info("DescribeDBInstances API Call")
            rds_describe = rds.describe_db_instances()
            for public_status in rds_describe['DBInstances']:
                if public_status['PubliclyAccessible'] == True:
                    public_rds = public_status['DBInstanceIdentifier']
                    logging.info("The following RDS instance is Publicly Accessible:")
                    print(public_rds)
                    public_db_list.append(public_rds)
            logging.info("Full list of public RDS instances:")
            print(public_db_list)
        except Exception as exception_handle:
            logging.error(exception_handle)
    logging.info("Full list of public RDS instances:")
    print(public_db_list)
    try:
        rds_single = boto3.client('rds')
        logging.info("Creating RDS Database for permissions check and CloudTrail event recording.")
        logging.info("CreateDBInstance API Call")
        dummy_rds = rds_single.create_db_instance(
            DBName='cloudsaga_db',
            DBInstanceIdentifier='cloudsagadbinstance',
            DBInstanceClass='db.t2.micro',
            AllocatedStorage=20,
            Engine='mysql',
            MasterUsername='awscostdb',
            MasterUserPassword=dummy_string,
            PubliclyAccessible=True,
            Tags=[
                {
                    'Key': 'CS-Purpose',
                    'Value': 'cs-costs'
                }
            ]
        )
        logging.info("RDS Database created.")
        logging.info("Deleting RDS Database that was just created.")
        logging.info("DeleteDBInstance API Call")
        dummy_rds_delete = rds_single.delete_db_instance(
            DBInstanceIdentifier='cloudsagadbinstance',
            SkipFinalSnapshot=True
        )
    except Exception as exception_handle:
        logging.error(exception_handle)


# Step 2. Attempt to create an S3 Bucket, and set as public.
def s3_check(unique_end):
    """Function to attempt making existing bucket public and creating a bucket and making public"""
    try:
        account_number = sts.get_caller_identity()["Account"]
        s3=boto3.client('s3')
        logging.info("Listing S3 Buckets...")
        logging.info("ListBuckets API Call")
        buckets=s3.list_buckets()
        logging.info("Creating bucket in %s" % account_number)
        logging.info("CreateBucket API Call")
        if region == 'us-east-1':
            new_bucket = s3.create_bucket(
                Bucket='cloudsaga-permission-test-' + account_number + '-' + unique_end
            )
        else:
            new_bucket = s3.create_bucket(
                Bucket='cloudsaga-permission-test-' + account_number + '-' + unique_end,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        logging.info("S3 Bucket cloudsaga-permission-test-" + account_number + "-" + unique_end + " created. Please ensure this bucket is deleted after the CloudSaga exercise has been completed, as it is publicly accessible.")
        # logging.info("PutBucketLogging API Call")
        # bucket_logging = s3.put_bucket_logging(
        #     Bucket='cloudsaga-permission-test-' + account_number,
        #     BucketLoggingStatus={
        #         'LoggingEnabled': {
        #             'TargetBucket': 'cloudsaga-permission-test-' + account_number,
        #             'TargetPrefix': 'cloudsagas3logs'
        #         }
        #     }
        # )
        logging.info("PutPublicAccessBlock API Call")
        bucket_private = s3.put_public_access_block(
            Bucket='cloudsaga-permission-test-' + account_number,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            },
        )
        logging.info("DeletePublicAccessBlock API Call")
        delete_public=s3.delete_public_access_block(
            Bucket='cloudsaga-permission-test-' + account_number,
        )
        logging.info("S3 Check Completed.")
    except Exception as exception_handle:
        logging.error(exception_handle)


def main():
    """Function that runs all of the previously defined functions"""
    dummy_string = random_pass()
    unique_end = random_string_generator()
    public_resource_check(region_list, dummy_string)
    s3_check(unique_end)
    logging.info("This is the end of the script. Please check and cleanup any resources created from this script.")