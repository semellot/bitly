import argparse
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
import requests


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

    decoded_response = response.json()
    return decoded_response['link']


def count_clicks(token, url):
    parsed_url = urlparse(url)
    bitlink_id = f"{parsed_url.netloc}{parsed_url.path}"
    api_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    decoded_response = response.json()

    return decoded_response['total_clicks']


def is_bitlink(token, url):
    parsed_url = urlparse(url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    api_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(api_url, headers=headers)

    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    received_args = parser.parse_args()

    url = received_args.url

    if is_bitlink(token, url):
        try:
            count_clicks = count_clicks(token, url)
        except requests.exceptions.HTTPError:
            print("Input bad link")
        print(f'Count of clicks: {count_clicks}')
    else:
        try:
            bitlink_url = shorten_link(token, url)
        except requests.exceptions.HTTPError:
            print("Input bad link")
        print(f'Short link: {bitlink_url}')
