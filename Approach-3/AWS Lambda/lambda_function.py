import configparser
import boto3
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration file path
oci_config_path = "config" # The configuration can come from Secrets

def read_config_from_file(file_path, client_type):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    return config[client_type.upper()]

def initialize_s3_client(file_path, client_type):
    
    try:
        config = read_config_from_file(file_path, client_type)
        region_name = config.get("region_name")
        access_key_id = config.get("access_key_id")
        secret_access_key = config.get("secret_access_key")
        endpoint_url = config.get("endpoint_url")
        
        s3 = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            endpoint_url=endpoint_url
        )
        return s3
    except Exception as e:
        logger.error(f"Error initializing S3 client: {e}")
        raise

def sync_new_files_from_oci_to_s3(oci_bucket_name, s3_bucket_name, s3_prefix, new_file):
    
    try:
        # Initialize OCI client
        oci_client = initialize_s3_client(oci_config_path, 'OCI')

        # Get object data from OCI bucket
        object_data = oci_client.get_object(Bucket=oci_bucket_name, Key=new_file)
        object_data_bytes = object_data['Body'].read()

        # Initialize S3 client
        s3_client = initialize_s3_client(oci_config_path, 's3')

        # Upload object to S3 bucket
        destination_object_key = s3_prefix + new_file
        s3_client.put_object(Body=object_data_bytes,
                             Bucket=s3_bucket_name,
                             Key=destination_object_key)

        return f'Sync file: {new_file} from {oci_bucket_name} into {s3_bucket_name}/{s3_prefix} successfully'
    except Exception as e:
        logger.error(f"Error syncing file from OCI to S3: {e}")
        raise

def lambda_handler(event, context):
    
    # Declare variables
    oci_bucket_name = 'StoreTest1'
    s3_bucket_name = 'oci-aws-test'
    s3_folder_prefix = 'approach-3/'
    
    try:
        # Retrieve created/updated object from SQS
        records = event['Records']
        responses = []
        for record in records:
            object_name = json.loads(record['body'])['resourceName']
        
            # Call method to sync files
            res = sync_new_files_from_oci_to_s3(oci_bucket_name, s3_bucket_name, s3_folder_prefix, object_name)
            responses.append(res)
            
        return {
            'statusCode': 200,
            'body': responses
        }
        
    except Exception as e:
        logger.error(f"Lambda function execution failed: {e}")
        return {
            'statusCode': 500,
            'body': f"Internal Server Error: {e}"
        }