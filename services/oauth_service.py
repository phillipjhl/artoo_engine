from settings import dev as config

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth
import base64

HOST: str = config.HOST
ARTOO_HUB_URL: str = config.ARTOO_HUB_URL

def get_oauth_token(client_id, client_secret):
    global HOST
    global ARTOO_HUB_URL
    # auth = base64.b64encode(b'{CLIENT_ACCESS_KEY}{CLIENT_SECRET_KEY}')
    HEADERS: dict = {'Content-Type': 'application/x-www-form-urlencoded', 'HOST': f'{HOST}'}
    BODY: dict = {'grant_type': 'client_credentials'}

    oauth_response = requests.post(f"{ARTOO_HUB_URL}/oauth2/token/", auth=HTTPBasicAuth(client_id, client_secret), headers=HEADERS, data=BODY)
    if oauth_response.status_code == 200:
        json = oauth_response.json()
        return json
    else:
        print(f"{oauth_response.json()}")

