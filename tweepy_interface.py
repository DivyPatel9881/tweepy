from requests import get, post
import urllib.parse
import base64
from json import loads

def base64_encode(message: str) -> str:
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')

def base64_decode(base64_message: str) -> str:
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')

def generate_bearer_token(consumer_key: str, consumer_secret_key: str) -> str:
    rfc_encoded_consumer_key = urllib.parse.quote(consumer_key)
    rfc_encoded_consumer_secret_key = urllib.parse.quote(consumer_secret_key)
    bearer_token_credential = rfc_encoded_consumer_key + ":" + rfc_encoded_consumer_secret_key
    base64_bearer_token_credential = base64_encode(bearer_token_credential)

    headers = dict()
    data = dict()
    headers['Authorization'] = 'Basic ' + base64_bearer_token_credential
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    data['grant_type'] = 'client_credentials'
    url = 'https://api.twitter.com/oauth2/token'

    response = post(url, headers=headers, data=data)
    response_dict = loads(response.text)
    return response_dict['access_token']

def get_tweets_from_tweet_ids(ids: list, bearer_token: str, custom_params: dict) -> list:
    headers = dict()
    headers['Authorization'] = 'Bearer ' + bearer_token
    params = dict()
    params_str = ''
    for id in ids:
        params_str += id + ","
    params_str = params_str[:-1]
    params['ids'] = params_str
    params.update(custom_params)
    url = 'https://api.twitter.com/labs/2/tweets'

    response = get(url, headers=headers, params=params)
    response_dict = loads(response.text)
    return response_dict['data']

def get_tweet_from_tweet_id(id: str, bearer_token: str, custom_params: dict) -> dict:
    headers = dict()
    headers['Authorization'] = 'Bearer ' + bearer_token
    params = dict()
    params.update(custom_params)
    url = 'https://api.twitter.com/labs/2/tweets' + id

    response = get(url, headers=headers, params=params)
    response_dict = loads(response.text)
    return response_dict['data']