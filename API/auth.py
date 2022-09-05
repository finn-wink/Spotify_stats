import base64
import requests
import datetime

client_id = 'ec391a53138f440da1ab2e2f9dbb9883'
client_secret = '68950a176080450ea34e6dd48ad1b81d'

token_url = 'https://accounts.spotify.com/api/token'
method = "POST"

token_data = {
    "grant_type" : "client_credentials"
}

client_creds = "{}:{}".format(client_id, client_secret)
client_creds_b64 = base64.b64encode(client_creds.encode())

token_header = {
    "Authorization" : "Basic {}".format(client_creds_b64.decode())
}

r = requests.post(token_url, data=token_data, headers=token_header)

print(r.json())

valid_request = r.status_code in range(200,299)

if valid_request:
    now = datetime.datetime.now()
    token_response_data = r.json()
    access_token = token_response_data['access_token']
    expires_in = token_response_data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now
