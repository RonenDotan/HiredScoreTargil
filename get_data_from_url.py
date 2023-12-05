import requests


def get_data(url):
    response = requests.get(url)
    decoded_content = response.content.decode("utf-8")
    return decoded_content
