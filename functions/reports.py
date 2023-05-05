import boto3
import untagged_resource

def lambda_handler(event, context):
    print(f"generating the untagged resources report and uploading ")
    untagged_resource.generate_report()

if __name__ == "__main__":
    event = {}
    context = {}
    lambda_handler(event, context)
    pass