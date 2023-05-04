import boto3
import untagged_resources

def lambda_handler(event, context):
    print(f"generating the untagged resources report and uploading ")
    untagged_resources.generate_report()

if __name__ == "__main__":
    event = {}
    context = {}
    lambda_handler(event, context)
    pass