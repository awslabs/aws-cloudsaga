# AWS CloudSaga - Simulate attacks in AWS
AWS CloudSaga is for customers to test security controls and alerts within their Amazon Web Services (AWS) environment, using generated alerts based on security events seen by the AWS Customer Incident Response Team (CIRT).

## Use Case
Security controls and best practices are published for securing AWS accounts, however, customers look for mechanisms to test security and incident response within their AWS environments, in order to protect themselves against known attacks. 

AWS CloudSaga is for customers who want to test their environment against documented attacks from the AWS CIRT. Using AWS CloudSaga, simple scenarios that mimic actual attacks can be run against a customer's environment, testing the customer's response plans and defenses when these events occur, and improve defenses of their AWS environment from the results.

## Usage
```
python3 cloudsaga.py



     ___   ____    __    ____   _______.     ______  __        ______    __    __   _______       _______.     ___       _______      ___      
    /   \  \   \  /  \  /   /  /       |    /      ||  |      /  __  \  |  |  |  | |       \     /       |    /   \     /  _____|    /   \     
   /  ^  \  \   \/    \/   /  |   (----`   |  ,----'|  |     |  |  |  | |  |  |  | |  .--.  |   |   (----`   /  ^  \   |  |  __     /  ^  \    
  /  /_\  \  \            /    \   \       |  |     |  |     |  |  |  | |  |  |  | |  |  |  |    \   \      /  /_\  \  |  | |_ |   /  /_\  \   
 /  _____  \  \    /\    / .----)   |      |  `----.|  `----.|  `--'  | |  `--'  | |  '--'  |.----)   |    /  _____  \ |  |__| |  /  _____  \  
/__/     \__\  \__/  \__/  |_______/        \______||_______| \______/   \______/  |_______/ |_______/    /__/     \__\ \______| /__/     \__\ 
                                                                                                                                               


            Joshua "DozerCat" McKiddy - Team DragonCat - AWS
            Type -h for help.

    usage: cloudsaga.py [-h] [--scenario SCENARIO] [--chapters] [--about ABOUT]

    CloudSaga - Simulate attacks based on previous Ziplines

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

## Scope


## Diagram

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
This scenario is based on the attack vector provided by IMDS version 1.
EC2 instances using IMDS version 1 are vulnerable to server side request
forgery (SSRF) attacks, and can be used as a pivot point for privilege
escalation within AWS.
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
Public Resources Scenario:
This scenario is for checking and creating public AWS resources within an AWS account.
This includes Amazon RDS and Amazon S3.
```


## Running the Code
The code in it's current form can be ran inside the following:
* AWS CloudShell (preferred)
* Locally (with IAM credentials, not preferred)


## Feedback
Please use the Issues section to submit any feedback, such as features or recommendations, as well as any bugs that are encountered.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.


## License

This project is licensed under the Apache-2.0 License.
