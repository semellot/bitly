from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
import os

def shorten_link(token, long_url):
    api_url = "https://api-ssl.bitly.com/v4/bitlinks"

    body = {
        'long_url': long_url
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(api_url, json=body, headers=headers)
    response.raise_for_status()

    json_url = response.json()
    return json_url['link']

def count_clicks(token, bitlink_id):
    api_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    json_bitlink = response.json()
    return json_bitlink['total_clicks']

def is_bitlink(token, url):
    bitlink = url.replace("https://","")
    api_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(api_url, headers=headers)
    if response.ok:
        return True

if __name__ == "__main__":
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    url = input('Input link: ')

    try:
        if is_bitlink(token, url):
            parsed_url = urlparse(url)
            bitlink_id = parsed_url.netloc+parsed_url.path
            count_clicks = count_clicks(token,bitlink_id)
            print(f'Count of clicks: {count_clicks}')
        else:
            bitlink_url = shorten_link(token, url)
            print(f'Short link: {bitlink_url}')

    except requests.exceptions.HTTPError:
        print("Input bad link")
