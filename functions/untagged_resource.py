import csv
import boto3
from datetime import datetime
session = boto3.Session()
ec2_cli = session.client('ec2')
s3 = session.client('s3')
sts_client = session.client("sts")
account_id = int(sts_client.get_caller_identity()["Account"])
CSV_FILE = 'untagged_resources.csv'
S3_BUCKET = f'{account_id}-enforce-tags-report'
def write_to_csv(dict_writer, resource_name, tags):
  row = dict(resource_name=resource_name, resource_tags=tags, date_reported=datetime.now())
  print(f"printing the row {row}")
  dict_writer.writerow(row)
def get_untagged_ec2():
  ec2_response = ec2_cli.describe_instances()
  ec2_arn = f'arn:aws:ec2:us-west-2:{account_id}:instance/'
  for response in ec2_response['Reservations']:
    for instance in response['Instances']:
      try:
        print(f"printing instance ", response['Instances'], type(response['Instances']))
        tag_response = ec2_cli.describe_tags(Filters=[
          {
            'Name': 'resource-id',
            'Values': [instance['InstanceId']]
          }
        ])
        if len(tag_response['Tags']) == 0:
          print(f"printing tags and instance ", tag_response['Tags'])
          write_to_csv(writer, ec2_arn+instance['InstanceId'], tag_response['Tags'])
      except Exception as ex:
        print(f"an error occurred in ec2: {ex}")
def generate_report():
  field_names = ['resource_name', 'resource_tags', 'date_reported']
  global writer
  with open(f'/tmp/{CSV_FILE}', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_MINIMAL,
                delimiter=',', fieldnames=field_names)
    writer.writeheader()

    get_untagged_ec2()
  
  s3.upload_file(f'/tmp/{CSV_FILE}', Bucket=S3_BUCKET, Key=f"reports/{CSV_FILE}")
  print(f"Report generated successfully at S3 bucket {S3_BUCKET} file = reports/{CSV_FILE}")
if __name__ == "__main__":
  generate_report()
  pass