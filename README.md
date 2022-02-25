# AWS CloudSaga - Simulate security events in AWS
AWS CloudSaga is for customers to test security controls and alerts within their Amazon Web Services (AWS) environment, using generated alerts based on security events seen by the AWS Customer Incident Response Team (CIRT).

## Use Case
Security controls and best practices are published for securing AWS accounts, however, customers look for mechanisms to test security and incident response within their AWS environments, in order to protect themselves against known security events. 

AWS CloudSaga is for customers who want to test their environment against documented security events from the AWS CIRT. Using AWS CloudSaga, simple scenarios that mimic actual security events can be run against a customer's environment, testing the customer's response plans and defenses when these events occur, and improve defenses of their AWS environment from the results.

## Usage
```
cloudsaga



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

    usage: cloudsaga.py [-h] [--scenario SCENARIO] [--chapters] [--about ABOUT]

    CloudSaga - Simulate security events based on previous Ziplines

    optional arguments:
    -h, --help           show this help message and exit
    --scenario SCENARIO  Perform the scenario you want to run against your AWS
                        environment.
    --chapters           List the available scenarios within CloudSaga. Use the
                        --about flag to read details about a specific scenario.
    --about ABOUT        Read about a specific scenario (e.g. --about
                        <scenario>. For a list of available scenarios, use the
                        --chapters flag.
```


## Prerequesites
### Permissions
The following permissions are needed within AWS IAM for CloudSaga to run:
* For imds-reveal:
```
"ec2:DescribeInstances"
```
* For network-changes:
```
"ec2:DescribeInstances",
"ec2:RunInstances",
"ec2:CreateVpc",
"ec2:DescribeVpcs",
"ec2:CreateSecurityGroup"
```
* For mining-bitcoin:
```
"ec2:DescribeInstances",
"ec2:RunInstances"
```
* For iam-credentials:
```
"iam:GenerateCredentialReport",
"iam:GetCredentialReport"
```
* For public-resources:
```
"rds:DescribeDBInstances",
"rds:CreateDBInstance",
"rds:DeleteDBInstance",
"s3:ListBuckets",
"s3:CreateBucket",
"s3:PutPublicAccessBlock",
"s3:DeletePublicAccessBlock"
```

## Specific Scenario Details
```
IMDS Reveal Scenario:
This scenario is based on a server-side request forgery attack. 
EC2 instances using IMDS version 1 are more likely to be subject to this 
kind of software flaw, and if EC2 Role credentials are present, those 
credentials can be used in AWS.
```
```
Bitcoin Mining Scenario:
This scenario simulates the creation of Bitcoin mining instances.
Attackers attempt to create Bitcoin mining instances using Amazon EC2,
in order to leverage legitimate AWS customer's resources for their own purposes.
```
```
Network Changes Scenario:
This scenario simulates the creation and modification of network resources within
AWS. This includes creating Amazon VPCs, as well as modifications to Security Groups,
for the purposes of compromising resources within the AWS account.
```
```
IAM Credentials Scenario:
This scenario attempts to grab the IAM credential report within the AWS account.
```
```
Publicly Accessible Resources Scenario:
This scenario is for creating then checking for publicly accessible resources within an AWS account.
```

## Running the Code
The code in it's current form can be ran inside the following:
* AWS CloudShell (preferred)
* Locally (with IAM credentials, not preferred)

## Prerequisites
The following prerequisites are required to use AWS CloudSaga
* Python 3.7 or later
* pip3 (for installation of AWS CloudSaga)

## Installing the code
Installation of the code is done via pip3:
```
pip3 install cloudsaga
```

## Step-by-Step Instructions (for running in AWS CloudShell)
1. Log into the AWS Console of the account you want to run AWS CloudSaga.
2. Click on the icon for AWS Cloudshell next to the search bar.
   * Ensure that you're in a region where AWS CloudShell is currently available.
3. Once the session begins, install AWS CloudSaga via pip3:
```
pip3 install cloudsaga
```
4. Once installed, run the following command to review the help page for AWS CloudSaga.
```
cloudsaga.py -h
```
5. Review the scenarios, select the one that you want to run for generating your security event for testing.

### Logging
A log file containing the detailed output of actions will be placed in the root directory of AWS CloudSaga. The format of the file will be cloudsaga_timestamp_here.log

Sample output within the log file:
```
2022-02-22 01:20:47,826 - INFO - --Checking instances in AWS region me-south-1--
2022-02-22 01:20:47,826 - INFO - DescribeInstances API Call in AWS region me-south-1--
2022-02-22 01:20:48,712 - INFO - You cannot perform lookup of IMDS versions in this region. Error message below:
2022-02-22 01:20:48,712 - ERROR - An error occurred (AuthFailure) when calling the DescribeInstances operation: AWS was not able to validate the provided access credentials
2022-02-22 01:20:48,713 - INFO - --Checking instances in AWS region sa-east-1--
2022-02-22 01:20:48,713 - INFO - DescribeInstances API Call in AWS region sa-east-1--
2022-02-22 01:20:49,525 - INFO - --Checking instances in AWS region us-east-1--
2022-02-22 01:20:49,525 - INFO - DescribeInstances API Call in AWS region us-east-1--
2022-02-22 01:20:49,876 - INFO - --Checking instances in AWS region us-east-2--
2022-02-22 01:20:49,876 - INFO - DescribeInstances API Call in AWS region us-east-2--
2022-02-22 01:20:50,192 - INFO - --Checking instances in AWS region us-west-1--
2022-02-22 01:20:50,192 - INFO - DescribeInstances API Call in AWS region us-west-1--
2022-02-22 01:20:50,444 - INFO - --Checking instances in AWS region us-west-2--
2022-02-22 01:20:50,445 - INFO - DescribeInstances API Call in AWS region us-west-2--
2022-02-22 01:20:50,610 - INFO - Instance ID i-99999999999999999 is using IMDSv1, where no authentication header is required to access the IMDS service.
```

## Cleaning Up
Once the logs have been enabled, you can safely remove any of the downloaded files from AWS CloudShell.
* Note: The log file containing the detailed output of actions will be in the root directory of AWS CloudSaga. If you want to retain this, please download this to a safe place, either locally or to an Amazon S3 bucket, for your records. For information on how to download files from AWS CloudShell sessions, refer to the following [link](https://docs.aws.amazon.com/cloudshell/latest/userguide/working-with-cloudshell.html#files-storage).

## Feedback
Please use the Issues section to submit any feedback, such as features or recommendations, as well as any bugs that are encountered.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
