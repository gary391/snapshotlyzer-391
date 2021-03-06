from setuptools import setup

setup(
    name='snapshotlyzer-391',
    version='0.1',
    author='gary391',
    author_email='gary391@gmail.com',
    description='snapshotlyzer-391 is a tool to manage AWS EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/gary391/snapshotlyzer-391',
    install_requires=[
        'click',
        'boto3',
        'prettytable',
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
        ''',
)
