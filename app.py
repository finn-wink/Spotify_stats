import sqlite3
import os
import json
import spotipy

from flask import Flask, render_template, request, redirect, session
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from requests import api
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from os import path
from datetime import datetime

from helper import login_required, RegisterForm, LoginForm, API_class


#Initializing a bunch of shit
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = ""

@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():

    """Homepage"""

    if request.method == "POST":
        return render_template("instruct.html")

    else:
        return render_template("index.html")


@app.route("/instruct", methods=["GET", "POST"])
@login_required
def instruct():

    #Uploading a file to the directory assigned to the user
    if request.method == "POST":
        user_string = str(session["user_id"])
        folder = 0
        for uploaded_file in request.files.getlist('json_file'):
            if uploaded_file.filename == '':
                return render_template("try_again.html")
            else:
                if folder == 0:
                    #get time and date
                    now = datetime.now()
                    dt_string = now.strftime("%Y%m%d%H%M%S")
                    
                    #make directory
                    dirName = "uploads/{}/{}".format(user_string, dt_string)
                    os.makedirs(dirName)
                    folder = 1

                #save into directory
                uploaded_file.save(os.path.join("uploads/{}/{}".format(user_string, dt_string), uploaded_file.filename))
        return render_template("success.html")

    return render_template("instruct.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logging in the user"""

    session.clear()

    form = LoginForm(request.form, csrf_enabled=False)

    if request.method == "POST" and form.validate_on_submit():
        username = form.username
        password = form.password
        s_username = str(username.data)
        s_password = str(password.data)

        con = sqlite3.connect('main.db')
        cur = con.cursor()
        
        #check if username exists
        if not cur.execute("SELECT username FROM users WHERE username = ( ? )",[ s_username ]):
            return render_template("no_username.html")
        
        #Check if the password matches for the username
        db_password_link = cur.execute("SELECT password FROM users WHERE username = ( ? )", [ s_username ])
        
        db_password = db_password_link.fetchall()

        if not check_password_hash(db_password[0][0], s_password):
            return render_template("incorrect_pass.html")

        #select id for session and save session id
        rows = cur.execute("SELECT id FROM users WHERE username = ( ? )", [ s_username ])

        id = rows.fetchall()

        session["user_id"] = id[0][0]
        
        user_string = str(session["user_id"])

        #creating directory for each user according to their user_id
        dirName = "uploads/{}".format(user_string)

        if not os.path.exists(dirName):
            os.makedirs(dirName)

        con.commit()

        return redirect("/")

    else:
        return render_template("login.html", form=form)
    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for new account
        and save data to the database """

    form = RegisterForm(request.form, csrf_enabled=False)

    if request.method == "POST" and form.validate_on_submit():
        
        #Accessing register class to place variables into database if the method is POST

        username = form.username
        password = form.password
        s_username = str(username.data)
        s_password = str(password.data)
        hash_password = generate_password_hash(s_password)

        con = sqlite3.connect('main.db')
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES ( ? , ? )", (s_username, hash_password))
        con.commit()
        
        return render_template("re_complete.html")

    else:
        return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """ Logout the user from the current session """

    session.clear()

    return redirect("/")

@app.route("/calculate", methods=["POST"])
@login_required
def calculate():
    """ This is where we read JSON files and make them into statistics for the user"""

    #Order and check for the newest file
    user_string = str(session["user_id"])
    directory = "uploads/{}".format(user_string)
    current_file = 0

    #check for the name of the newest folder
    for filename_s in os.listdir(directory):
        filename = int(filename_s)
        if filename > current_file:
            current_file = filename

    if current_file == 0:
        return render_template("try_again_nofile.html")
    
    #Access json files and add them together into one dictionary
    folder = str(current_file)
    folder_dir = "uploads/{}/{}".format(user_string, folder)
    
    TrackList = []
    song_dict = {}

    for file in os.listdir(folder_dir):
        json_path = os.path.join(folder_dir, file)
        f = open('{}'.format(json_path), encoding="utf8")
        data = json.load(f)
        for things in data:
            TrackList.append(things)

    #List with all the song titles
    songs_played = []
    artists_played = []
    

    for songs in TrackList:
        if songs['trackName'] in songs_played and songs['artistName'] == artists_played[songs_played.index(songs['trackName'])] or songs['trackName'] == 'Unknown Track':
            continue

        else:
            songs_played.append(songs['trackName'])
            artists_played.append(songs['artistName'])

    clean_songs_played = songs_played
    amount_played = [1] * len(songs_played)

    for items in TrackList:
        if items['trackName'] in songs_played and items['artistName'] == artists_played[songs_played.index(items['trackName'])]:
            amount_played[songs_played.index(items['trackName'])] += 1

    lists = zip(songs_played, artists_played, amount_played)
    songs_played, artists_played, amount_played = zip(*sorted(lists, key=lambda x : x[2], reverse=True))

    headings = ['Song Title', 'Artist Name', 'No. of Plays']

    data = []
    artist_ids = []
    counter = 0

    for favs in range(9):
        added = []
        song = songs_played[favs]
        artist = artists_played[favs]
        num = amount_played[favs]
        added.append(song)
        added.append(artist)
        added.append(num)
        data.append(added)

        if counter < 5:
            spotify_class = API_class()
            api_return = spotify_class.search_artists(artist)
            artist_id = api_return['artists']['items'][0]['id']
            artist_ids.append(artist_id)
            counter +=1
        
    spotify_class = API_class()
    recommend = spotify_class.recommend_me(artist_ids)
    
    data_3 = []
    headings_3 = ['Song title', 'Artist Name', 'Album']
    
    for tracks in recommend['tracks']:
        added = []
        recommend_album = tracks['album']['name']
        recommend_track = tracks['name']
        recommend_artist = tracks['album']['artists'][0]['name']
        added.append(recommend_track)
        added.append(recommend_artist)
        added.append(recommend_album)
        data_3.append(added)

    #calculate the songs that were skipped the most
    songs_skipped = [0] *len(songs_played)
    
    for times in TrackList:
        if times['msPlayed'] < 3000 and times['trackName'] in songs_played and times['artistName'] == artists_played[songs_played.index(times['trackName'])]:
            songs_skipped[songs_played.index(times['trackName'])] += 1

    list = zip(songs_played, artists_played, songs_skipped)
    songs_played, artists_played, songs_skipped = zip(*sorted(list, key=lambda x : x[2], reverse=True))

    headings_2 = ['Song Title', 'Artist Name', 'No. of Skips']

    data_2 = []
    for favs in range(9):
        added = []
        song = songs_played[favs]
        artist = artists_played[favs]
        num = songs_skipped[favs]
        added.append(song)
        added.append(artist)
        added.append(num)
        data_2.append(added)
    
    return render_template("statistics.html", headings=headings, data=data, headings_2=headings_2, data_2=data_2, headings_3=headings_3, data_3=data_3)





