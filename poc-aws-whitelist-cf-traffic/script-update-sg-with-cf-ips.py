import boto3
from botocore.exceptions import ClientError

# Set the region and security group ID
region_name = 'us-east-1'
security_group_id = 'sg-123456789'

# Get the current CloudFront IP ranges
cloudfront_ips = []
try:
    client = boto3.client('cloudfront')
    response = client.list_cloud_front_ip_ranges()
    for ip_range in response['CloudFrontIPList']['Items']:
        if ip_range['IPVersion'] == 'IPv4':
            cloudfront_ips.append(ip_range['CIDR'])
except ClientError as e:
    print('Error getting CloudFront IP ranges: ' + str(e))
    exit()

# Authorize inbound traffic from the CloudFront IP ranges
try:
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': ip} for ip in cloudfront_ips]
            }
        ]
    )
    print('Inbound traffic from CloudFront IP ranges authorized on port 80')
except ClientError as e:
    print('Error authorizing inbound traffic: ' + str(e))
    exit()