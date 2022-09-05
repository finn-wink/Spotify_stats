import os
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators
from flask import redirect, render_template, request, session
from functools import wraps
from flask_wtf import Form, CsrfProtect, FlaskForm
from flask_wtf.file import FileField, FileRequired
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

#This is for additional functions

csrf = CsrfProtect()

class RegisterForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

class API_class:
    def search_artists(self, artist):
        #searching for the particular artist and returning it
        client_id = 'ec391a53138f440da1ab2e2f9dbb9883'
        client_secret = '68950a176080450ea34e6dd48ad1b81d'

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        result = sp.search(artist, type="artist")
        return result

    def recommend_me(self, artist_ids):
        #take the list of artists and generate recommendations
        client_id = 'ec391a53138f440da1ab2e2f9dbb9883'
        client_secret = '68950a176080450ea34e6dd48ad1b81d'

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        recomms = sp.recommendations(seed_artists=artist_ids, limit=10)

        return recomms