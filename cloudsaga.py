#// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0
# AWS CloudSaga - Simulate security events in AWS
# Joshua "DozerCat" McKiddy - Customer Incident Response Team (CIRT) - AWS


import logging
import boto3
import time
import datetime
import argparse
from botocore.exceptions import ClientError
from datetime import timezone
from scenarios import iam_credentials, imds_reveal, mining_bitcoin, network_changes, public_resources


current_date = datetime.datetime.now(tz=timezone.utc)
current_date_string = str(current_date)
timestamp_date = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H%M%S")
timestamp_date_string = str(timestamp_date)


logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
output_handle = logging.FileHandler('cloudsaga_' + timestamp_date_string + '.log')
output_handle.setLevel(logging.INFO)
logger.addHandler(output_handle)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
output_handle.setFormatter(formatter)


def banner():
    """Function to run the AWS CloudSaga banner"""
    print('''


     ___   ____    __    ____   _______.          
    /   \  \   \  /  \  /   /  /       |         
   /  ^  \  \   \/    \/   /  |   (----`       
  /  /_\  \  \            /    \   \         
 /  _____  \  \    /\    / .----)   |      
/__/     \__\  \__/  \__/  |_______/       

  ______  __        ______    __    __   _______       _______.     ___       _______      ___
 /      ||  |      /  __  \  |  |  |  | |       \     /       |    /   \     /  _____|    /   \ 
|  ,----'|  |     |  |  |  | |  |  |  | |  .--.  |   |   (----`   /  ^  \   |  |  __     /  ^  \ 
|  |     |  |     |  |  |  | |  |  |  | |  |  |  |    \   \      /  /_\  \  |  | |_ |   /  /_\  \ 
|  `----.|  `----.|  `--'  | |  `--'  | |  '--'  |.----)   |    /  _____  \ |  |__| |  /  _____  \  
 \______||_______| \______/   \______/  |_______/ |_______/    /__/     \__\ \______| /__/     \__\ 
                                                                                                                                               


            Joshua "DozerCat" McKiddy - Team DragonCat - AWS
            Type -h for help.
    '''
    )


def main():
    """Main function to run the code"""
    output_handle = logging.FileHandler('cloudsaga_' + timestamp_date_string + '.log')
    output_handle.setLevel(logging.INFO)
    logger.addHandler(output_handle)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    output_handle.setFormatter(formatter)

    parser = argparse.ArgumentParser(description='AWS CloudSaga - Simulate security events in AWS')
    parser.add_argument('--scenario',help=' Perform the scenario you want to run against your AWS environment.', required=False)
    parser.add_argument('--chapters',help=' List the available scenarios within CloudSaga. Use the --about flag to read details about a specific scenario.', action='store_true', required=False)
    parser.add_argument('--about',help=' Read about a specific scenario (e.g. --about <scenario>. For a list of available scenarios, use the --chapters flag.', required=False)


    args = parser.parse_args()
    banner()

    if args.chapters:
        print('''
        Chapters:
        imds-reveal: IMDS Reveal discovers instances that using IMDS v1, which are vulnerable to the IMDSv1 attack vector.
        mining-bitcoin: Uses Amazon EC2 resources to simulate creation of Bitcoin mining.
        network-changes: Uses Amazon VPC resources to simulate network changes.
        iam-credentials: Attempts to grab the IAM credential report within the AWS account.
        public-resources: Checks Amazon RDS and Amazon S3 for resources that are public, as well as creates a public RDS instance.
        ''')
        return

    elif args.about == 'imds-reveal':
        print('''
        IMDS Reveal Scenario:
        This scenario is based on the attack vector provided by IMDS version 1.
        EC2 instances using IMDS version 1 are vulnerable to server side request
        forgery (SSRF) attacks, and can be used as a pivot point for privilege
        escalation within AWS.

        Resources Checked:
        Amazon EC2
        ''')
    
    elif args.about == 'mining-bitcoin':
        print('''
        Bitcoin Mining Scenario:
        This scenario simulates the creation of Bitcoin mining instances.
        Attackers attempt to create Bitcoin mining instances using Amazon EC2,
        in order to leverage legitimate AWS customer's resources for their own purposes.

        Resources Checked:
        Amazon EC2
        ''')

    elif args.about == 'network-changes':
        print('''
        Network Changes Scenario:
        This scenario simulates the creation and modification of network resources within
        AWS. This includes creating Amazon VPCs, as well as modifications to Security Groups,
        for the purposes of compromising resources within the AWS account.

        Resources Checked:
        Amazon VPC
        Amazon EC2
        ''')

    elif args.about == 'iam-credentials':
        print('''
        IAM Credentials Scenario:
        This scenario attempts to grab the IAM credential report within the AWS account.

        Resources Checked:
        Amazon IAM
        ''')

    elif args.about == 'public-resources':
        print('''
        Public Resources Scenario:
        This scenario is for checking and creating public AWS resources within an AWS account.
        This includes Amazon RDS and Amazon S3.

        Resources Checked:
        Amazon RDS
        Amazon S3
        ''')


    if args.scenario == 'imds-reveal':
        imds_reveal.main()
    elif args.scenario == 'mining-bitcoin':
        mining_bitcoin.main()
    elif args.scenario == 'network-changes':
        network_changes.main()
    elif args.scenario == 'iam-credentials':
        iam_credentials.main()
    elif args.scenario == 'public-resources':
        public_resources.main()
    else:
        print("No options selected. Please run -h for help.")


if __name__ == '__main__':
    main()