# Statify: Your personal listening statistics

#### Video Demo:  <URL HERE>

#### Description:
##### The idea:
The idea for this project came when I saw a video about individuals downloading their Google data,
specifically the json files that were returned to them from the Google server. I quickly began to 
research what other services provided you the opportunity to download your own user data and stumbled
upon Spotify. I'm quite an avid music listener and was interested in exploring the data I might be 
able to find in my personal spotify files. I realized that if I was interested in this, maybe others 
would too and therefore decided to write a web app using Flask, that would analyze the json files
through Python and generate a website layout of various statistics. 

##### How it works:
The web application was written using python, flask, html and css. The way that flask was set up to 
dynamically generate parts of the webpages is quite similar to the previous assignment posed in the
course.
Starting on the flask side of things, there is the app.py file. This file is the main file of the 
entire project and provides all the linkages to various pages, as well as various functions and 
basic setups for the webpage. There is an additional file, helper.py, which houses some of the 
various functions that are used within the website. I think if I could rewrite the code, I would
make use of classes a lot more from the beginning on in order to keep app.py a lot more clean. However,
I only started to truly use classes when developing the last few functions and was only then confident
with it, but I guess you learn as you go. 
Focusing down on the actual functions of the website, it is easiest to go through it step by step.
#1 The user is prompted to login or register on the webpage, which is saved to an SQL database
#2 The user is shown the homepage and is able to move to the upload site. Any other link will
simply link you to the upload site or a site with an error, since no file has been submitted by
the user yet.
#3 The user is shown instructions on how to upload their file to the system and which files to upload
#4 The users files are stored on a server, within a personal folder, which is date and time stamped in
order to make sure it is easy to find the newest files of each user
#4.1 On the upload page, there is the possibility to use the most recent file, which will look up
the newest folder and submit those into the calculation query.
#5 The users files are scanned by the python file and basic statistics are calculated through the use
of various functions
#6 Parts of the results are passed into an API query that connects to the spotify database in order to
ask for a recommendation of songs according to the spotify AI prediction.
#6.1 This API query uses the users top 5 artists in order to find 10 suitable songs that the user might like
#7 The statistics for the user are displayed on a statistics page using HTML tables

##### Additional ideas:
There are still a lot of ideas on how to improve the experience of the website and also make the code
a lot cleaner than it is. However, at the moment, the project has come to a part where it is definitely
already usable and has been tested on various subjects. I'm proud to give it an early release alpha title
for now. 