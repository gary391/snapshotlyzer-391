# snapshotlyzer-391

Demo project to manage AWS EC2 instances snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created by the AWS CLI.

`aws configure --profile shotty`


## Running

`pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>`

*command* is instances, volumes or snapshots
*subcommand* - depends on command
*project* is optional

## Example Output:
```
+---------------------+---------------+------------------+----------------+-------------------------------------------+
|     Instance-Id     | Instance-Type | AvailabilityZone | Instance-state |              Public-DNS-Name              |
+---------------------+---------------+------------------+----------------+-------------------------------------------+
| i-06f1e69890f6c0345 |    t2.micro   |    us-east-1d    |    running     | ec2-54-164-76-112.compute-1.amazonaws.com |
| i-07ab3c3e0a5f48062 |    t2.micro   |    us-east-1d    |    running     |  ec2-3-92-223-10.compute-1.amazonaws.com  |
| i-05fffa25618742cb2 |    t2.micro   |    us-east-1d    |    running     |  ec2-3-83-175-125.compute-1.amazonaws.com |
| i-09251631099eb4ca0 |    t2.micro   |    us-east-1d    |    running     |  ec2-3-87-208-243.compute-1.amazonaws.com |
| i-09d126ab12999580d |    t2.micro   |    us-east-1d    |    running     |  ec2-3-92-65-133.compute-1.amazonaws.com  |
+---------------------+---------------+------------------+----------------+-------------------------------------------+
```
