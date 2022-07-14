#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate security events in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS


import logging
import boto3
import datetime
from datetime import timezone


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


def get_cred_report():
    """Function to retrieve credential report"""
    try:
        iam_user=boto3.client('iam', region_name='us-east-1') #May need to change region name
        logging.info('Generating credential report')
        iam_user.generate_credential_report()
        logging.info('Getting credential report')
        get_cred=iam_user.get_credential_report()
        logging.info("IAM Credential Report generated/retrieved.")
    except Exception as exception_handle:
        logging.error(exception_handle)
        logging.info("IAM Credential Report could not be generated/retrieved.")


def main():
    """Function that runs all of the previously defined functions"""
    get_cred_report()
    logging.info("This is the end of the script. Please check and cleanup any resources created from this script.")
