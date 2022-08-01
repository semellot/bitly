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

    bitlink = response.json()
    return bitlink['link']


def count_clicks(token, url):
    parsed_url = urlparse(url)
    bitlink_id = f"{parsed_url.netloc}{parsed_url.path}"
    api_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    bitlink = response.json()

    return bitlink['total_clicks']


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

    url = input('Input link: ')

    try:
        if is_bitlink(token, url):
            count_clicks = count_clicks(token, url)
            print(f'Count of clicks: {count_clicks}')
        else:
            bitlink_url = shorten_link(token, url)
            print(f'Short link: {bitlink_url}')

    except requests.exceptions.HTTPError:
        print("Input bad link")
