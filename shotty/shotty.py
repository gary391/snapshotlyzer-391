import boto3
import click
import botocore
from prettytable import PrettyTable
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
        # print(instances)
    else:
        instances = ec2.instances.all()

    return instances


def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())  # lists by default the most recent snapshot
    return snapshots and snapshots[0].state == 'pending'


@click.group()
def cli():
    """ Shotty manages snapshots"""


@cli.group('snapshots')
def snapshots():
    """ Commands for snapshots"""


@snapshots.command('list')  # decorator in python decorate/warp functions
@click.option('--project', default=None, help="Only snapshots for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True, help="List all snapshots for each volume, not just the most recent")
def list_snapshots(project, list_all):
    "List EC2 snapshots"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ". join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))

                if s.state == 'completed' and not list_all:  # by default lists the most recent snapshots
                    break
    return


@cli.group('volumes')
def volumes():
    """ Commands for volumes"""


@volumes.command('list')  # decorator in python decorate/warp functions
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)
    table = PrettyTable(["Volume-Id", "Instance-Id", "Volume-State",
                         "Volume-Size", "Volume-Encryption"])
    for i in instances:
        for v in i.volumes.all():
            # print(", ". join((
            #     v.id,
            #     i.id,
            #     v.state,
            #     str(v.size) + "GiB",
            #     v.encrypted and "Encrypted" or "Not Encrypted"
            # ))
            # return
            table.add_row([v.id, i.id, v.state, str(v.size) + "GiB",
                           v.encrypted and "Encrypted" or "Not Encrypted"])
    print(table)


@cli.group('instances')
def instances():
    """ Commands for instances"""


# decorator in python decorate/warp functions
@instances.command('snapshot', help="Create snapshots for all volumes")
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping...{0}".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print(" skipping {0}, snapshot already in progress". format(v.id))
                continue
            print("Creating snapshots of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshotlyzer-391")
        print("Starting...{0}".format(i.id))
        i.start()
        i.wait_until_running()

    print("Job Well Done!")

    return


@instances.command('list')  # decorator in python decorate/warp functions
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)
    table = PrettyTable(["Instance-Id", "Instance-Type", "AvailabilityZone",
                         "Instance-state", "Public-DNS-Name", "project"])

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        # print(tags)
        # print(tags.get('Project', '<no project>'))

        # print(i)
        # print(', '.join((i.id, i.instance_type,
        #                  i.placement['AvailabilityZone'], i.state['Name'],
        #                  i.public_dns_name, tags.get('Project', '<no project>')
        #                  )))
        # return
        table.add_row([i.id, i.instance_type, i.placement['AvailabilityZone'],
                       i.state['Name'], i.public_dns_name, tags.get('Project', '<no project>')])

    print(table)


@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue  # no need to continue, as the loop will continue itself.
    return


@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}. ".format(i.id) + str(e))
            continue  # no need to continue, as the loop will continue itself.
    return


if __name__ == '__main__':
    cli()
