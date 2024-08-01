import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def create_s3_bucket(bucket_name, region=None):
    try:
        # Create an S3 client
        s3_client = boto3.client('s3', region_name=region)
        
        # Create the bucket
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
        print(f"Bucket {bucket_name} created successfully.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Failed to create bucket {bucket_name}: {e}")

# Specify the bucket name and region
bucket_name = 'terravar'
region = 'us-west-2'  # Specify your preferred region

# Create the bucket
create_s3_bucket(bucket_name, region)
