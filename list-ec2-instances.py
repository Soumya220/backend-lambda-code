import boto3
from pprint import pprint 
aws_management_console = boto3.session.Session(profile_name="default")
ec2_console =  aws_management_console.client("ec2")
result = ec2_console.describe_instances()
pprint(result['Reservations'])

