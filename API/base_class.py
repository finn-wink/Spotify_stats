import base64
import requests
import datetime
from urllib.parse import urlencode

client_id = 'ec391a53138f440da1ab2e2f9dbb9883'
client_secret = '68950a176080450ea34e6dd48ad1b81d'

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'


    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """returns a base64 string """
        client_id = self.client_id
        client_secret = self.client_secret
        
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id or client_secret")

        client_creds = "{}:{}".format(client_id, client_secret)
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization" : "Basic {}".format(client_creds_b64)
        }

    
    def get_token_data(self):
        return {
            "grant_type" : "client_credentials"
        }   

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        
        r = requests.post(token_url, data=token_data, headers=token_header) 
        if r.status_code not in range(200,299):
            raise Exception("Could not authenticate client")

        now = datetime.datetime.now()
        token_response_data = r.json()
        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_did_expire = expires < now
        self.access_token_expires = expires
        return True

client = SpotifyAPI(client_id, client_secret)

client.perform_auth()

access_token = client.access_token

header = {
    "Authorization": "Bearer {}".format(access_token)
}


