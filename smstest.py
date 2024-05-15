
import requests


def send_sms_api(  message, 
             recipients, 
              ):
    content_type="application/json"
    schedule_time=None
    recipient_id=None
    dest_addr=None
    encoding=0
    source_addr = "INFO"
    api_key = "8d069829168328d7"
    secret_key = "NjEzY2YwMjdiYjM4YzU3OTY0ZGIxYzcyZmVkNDcyNTcwZTAxOTkxMzI3ZDM2OTNkYjYxMjc1NmVjOTE4MTRkYg=="
    
    url = "https://apisms.beem.africa/v1/send"
    headers = {
        "Content-Type": content_type
    }
    auth = (api_key, secret_key)
    data = {
        "source_addr": source_addr,
        "message": message,
        "recipients": recipients,
        "encoding": encoding
    }
    if recipient_id:
        data["recipient_id"] = recipient_id
    if dest_addr:
        data["dest_addr"] = dest_addr
    if schedule_time:
        data["schedule_time"] = schedule_time

    response = requests.post(url, headers=headers, auth=auth, json=data)
    
    return response.json()

message = "Hello from Beem Africa!"
recipients = ["255621189850"] 
response = send_sms_api(message, recipients)
print(response)