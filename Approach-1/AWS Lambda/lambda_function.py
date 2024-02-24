def lambda_handler(event, context):
    # Extract keys from S3 event
    s3_event_records = event.get('Records', [])
    keys = [record['s3']['object']['key'] for record in s3_event_records]
    
    print(keys)