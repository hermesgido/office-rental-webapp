def send_sms(number, message):
    import requests
    from requests.auth import HTTPBasicAuth
    url = "https://apisms.beem.africa/v1/send"

    data = {
        "source_addr": "INFO",
        "encoding": 0,
        "message": message,
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": f"{number}"
            }
        ]
    }
    password = "MGVjMjVhOTQ1N2U0MmM2MzQwNjc2YzI3MjdiMzk2YzViZjVhNDcyZGRkODViMDc3MGFlYTkzYzQ1YTAyMjAwZg=="
    username = "ce64e6750d9de50e"

    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        print("SMS sent successfully!")
    else:
        print("SMS sending failed. Status code:", response.status_code)
        print("Response:", response.text)
