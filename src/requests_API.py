import requests
import time
import logging
import json

FAILED_THRESHOLD = 10


def GPT4_requests(query):
    pass


def get_access_token_wenxinyiyan(client_id, client_secret):
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    res_json = json.loads(response.text)
    return res_json['access_token']


def WenXinYiYan4_requests(query):
    API_KEY = ""
    SECRET_KEY = ""

    app_token = ''

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + app_token

    response_log = str.upper("response_log")

    payload = json.dumps({
        "temperature": 0.95,
        "top_p": 0.8,
        "penalty_score": 1.0,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    failed_count = 0
    while True:
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            text = json.loads(response.text)
            response_log = json.dumps(text)
            return text['result']

        except Exception as e:
            failed_count += 1
            logging.error(response_log)
            logging.error(e)
            if failed_count >= FAILED_THRESHOLD:
                break
            time.sleep(1)
    return response_log
