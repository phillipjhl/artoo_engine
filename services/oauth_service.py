from settings import dev as config

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth
import base64

HOST: str = config.HOST

def get_oauth_token(client_id, client_secret):
    # auth = base64.b64encode(b'{CLIENT_ACCESS_KEY}{CLIENT_SECRET_KEY}')
    HEADERS: dict = {'Content-Type': 'application/x-www-form-urlencoded', 'HOST': f'{HOST}'}
    BODY: dict = {'grant_type': 'client_credentials'}

    oauth_response = requests.post("http://127.0.0.1:8000/oauth2/token/", auth=HTTPBasicAuth(client_id, client_secret), headers=HEADERS, data=BODY)

    if oauth_response.status_code == 200:
        json = oauth_response.json()
        return json

