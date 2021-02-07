from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

def get_oauth2_token(client_id, client_secret):
    auth = HTTPBasicAuth(client_id, client_secret)

    client = BackendApplicationClient(client_id=client_id)

    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(token_url='https://127.0.0.1:8000/oauth2/token/', auth=auth)

    print(token)

