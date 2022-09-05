import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

client_id = {spotify client id}
client_secret = {spotify secret id}

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

name = "{Artist Name}" #chosen artist
result = sp.search(name, type="artist") #search query
result['tracks']['items'][0]['artists']
