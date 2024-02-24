import requests
import json

def handler(context, data):
    try:
        # Parsing JSON data
        content = json.loads(data.getvalue())

        # Extract necessary fields
        data_payload = content.get("data")
        resource_name = data_payload.get("resourceName")

        # Building payload for HTTP request
        payload = {
            'data': data_payload,
            'resourceName': resource_name
        }
        
        # HTTP request to trigger AWS Lambda via API Gateway
        request_rclone = requests.post("URL/oci-sync-test", json=payload)

        # Check HTTP response status code
        if request_rclone.status_code != 200:
            raise ValueError(f"HTTP request failed with status code {request_rclone.status_code}")

        return {"message": "Sync completed."}
    
    except Exception as e:
        # Log and return error message
        error_message = f"Error: {str(e)}"
        print(error_message)
        return {"error": error_message}
