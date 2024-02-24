import subprocess
import json
import os

def handler(context, data):
    try:
        # Parse JSON data from OCI event
        content = json.loads(data.getvalue())

        # Extract object name and suffix
        object_name = content["data"]["resourceName"]
        suffix = os.path.dirname(object_name)

        # Construct rclone command
        rclone_command = f"rclone sync oci:StoreTest1/{object_name} s3:oci-aws-test/approach-1/{suffix}"

        # Run rclone command to sync objects from OCI bucket to AWS S3 bucket
        subprocess.run(rclone_command, shell=True, check=True)

        return {"message": "Sync completed."}

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return {"error": error_message}
