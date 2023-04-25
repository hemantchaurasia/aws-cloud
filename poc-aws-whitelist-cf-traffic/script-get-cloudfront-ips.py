import boto3

cloudfront = boto3.client('cloudfront')
response = cloudfront.list_cloud_front_ip_ranges()
ipv4_ranges = response['CloudFrontIPList']['Items']
ipv4_ranges = [item['CIDR'] for item in ipv4_ranges if item['IPVersion'] == 'IPv4']

print(ipv4_ranges)