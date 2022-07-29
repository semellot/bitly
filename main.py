from dotenv import load_dotenv
import requests
import json
import os

token = os.environ['TOKEN']

def shorten_link(token, long_url):
    url_api = "https://api-ssl.bitly.com/v4/bitlinks"

    body = {
        'long_url': long_url
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url_api, json=body, headers=headers)
    response.raise_for_status()

    json_url = json.loads(response.text)
    return json_url['link']

def count_clicks(token, bitlink_id):
    url_api = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_api, headers=headers)
    response.raise_for_status()

    json_bitlink = json.loads(response.text)
    return json_bitlink['total_clicks']

def is_bitlink(url):
    if "https://bit.ly/" in url:
        return True

if __name__ == "__main__":
    load_dotenv()
    url = input('Input link: ')

    try:
        if is_bitlink(url):
            bitlink_id = url.replace("https://","")
            count_clicks = count_clicks(token,bitlink_id)
            print(f'Count of clicks: {count_clicks}')
        else:
            bitlink_url = shorten_link(token, url)
            print(f'Short link: {bitlink_url}')

    except requests.exceptions.HTTPError:
        print("Input bad link")
