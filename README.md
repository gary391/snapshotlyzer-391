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
