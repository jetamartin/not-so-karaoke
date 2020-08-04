# For parsing duration of videos 
from isodate import parse_duration

# For parsing coverting characters in video titles (e.g. &39 to ')
import html.parser as htmlparser
from utilities import *
from constants import *
from messages import *

# import pickle
from sqlalchemy import exc

import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm, SignupForm, LoginForm

from models import db, connect_db, User, Favorite
# from secrets import API_SECRET_KEY


app = Flask(__name__)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///nskdb'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['API_SECRET_KEY'] = os.environ.get('API_SECRET_KEY', YOUTUBE_API_KEY)
app.config['YOUTUBE_API_KEY'] = os.environ.get('YOUTUBE_API_KEY', YOUTUBE_API_KEY)

app.config.update(SESSION_COOKIE_SAMESITE='Lax')
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
  """ Present App 404 page if user manually enters invalid route """
  return render_template('404.html')

@app.route('/')
def home():
  """ Displays the app's home/index page """
  return render_template("/index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  """ Signup user: produce form and handle submission"""

  form = SignupForm()

  if form.validate_on_submit():
    name = form.username.data
    password = form.password.data 
    email = form.email.data
    
    try:
      user = User.signup(name, password, email) 
      db.session.add(user) 
      db.session.commit()
    except exc.IntegrityError:
      print("Failure to create user...perhaps a duplicate user name")
      form.username.errors = ["Bad name/password"]
      flash(USERNAME_TAKEN, "error")
      return render_template("/signup.html", form=form)
    else: 
      session["user_id"] = user.id
      session["username"] = user.username
      flash(f"{user.username.capitalize()}, {ACCOUNT_CREATED}", "success")
      return redirect("/search")

  else: # There was an error on the form

    return render_template("/signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Produce login form or handle login. """
    form = LoginForm()

    if form.validate_on_submit():
      name = form.username.data    
      password = form.password.data  

      # authenticate will return a user or False
      user = User.authenticate(name, password)

      if user:
        flash(f"{user.username.capitalize()}, {LOGIN_SUCCESSFUL}", "success")

        session["user_id"] = user.id # keep logged in
        session["username"] = user.username
        return redirect("/search")
      else:
        form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route('/search', methods=['GET', 'POST'])
def index():
  """ Displays video search form and subsequent search results """

  form = SearchForm()
 
  if form.validate_on_submit():

    # Get values entered on Video Search screen
    artist = form.artist.data.strip()
    song = form.song.data.strip()

    # Save search values as Session variables
    session['artist'] = artist
    # if user included song then save that in session
    # if (song.strip()):
    session['song'] = song

    # Calls the YT API to retrieve videos matching  search criteria
    search_results = search_for_matching_videos(artist, song)
    
     # Check to see if error encountered while making API call
    if search_results['status'] == 'error':

      session['artist'] = ""
      session['song'] = ""
      return redirect('/search')

    else: # YT API returned success status code

      json_results = search_results['results']

      # if api request was successful but no videos found matching search criteria then notify user
      if len(json_results) == 0:

        flash(NO_MATCHING_VIDEOS, "error")
        return redirect('/search')

      # Save the YT video search results (video_id, title, thumbnail) and check to see if video is a current favorite
      video_search_results = process_video_search_results (json_results, 'video_search')

      # Get artist and Song entered on search form
      artist_input = session.get('artist', None)
      song_input = session.get('song', None)

      # For each video in video_search_results build a list of video_detail_objects so results can be displayed
      video_detail_objects_list = build_list_of_video_objects(video_search_results)

      return render_template('/search.html', form=form, videos = video_detail_objects_list)

  else:

    return render_template("/search.html", form=form)


@app.route('/video/<video_id>')
def viewVideo(video_id):
  """ Allows the user to view the selected video  """

   
  # Call YT Video Detail API to get video details 
  search_results = get_detailed_video_data(video_id)
 
  if (search_results['status'] == 'error'):
    return redirect('/search')

  else: # YT API returned success status code

    json_results = search_results['results']

    # if api request was successful but no videos found matching search criteria then notify user
    if len(json_results) == 0:
      flash(NO_MATCHING_VIDEOS, "error")
      return redirect('/search')

  # Extract the detailed video information from the JSON Data returned from the YT API call 
  video = build_video_object(search_results['results'], 'video_detail')

  # Get artist and Song entered on search form
  artist_input = session.get('artist', None)
  song_input = session.get('song', None)

  # Use search inputs plus heuristics to derive artist and song title (remember song_title is not required search input)
  artist_and_song_title = get_artist_and_song(artist_input, song_input, video.title)

  # Retrieve the lyrics
  lyrics = get_lyrics(artist_and_song_title['artist'], artist_and_song_title['song'] )

  # Build a detail video object to simplify passing data into view
  video_details = create_detail_video_object(video, artist_and_song_title)

  return render_template('/view-video.html', video_details = video_details, lyrics = lyrics)


@app.route('/lyrics', methods=['POST'])
def getMoreLyrics():
  """ Allows user to manually search for lyrics (from the view-video screen) if no matching lyrics found the original search  """
  artist = request.json['artist']
  song = request.json['song']
  lyrics = get_lyrics(artist, song)
  return jsonify(lyrics)


@app.route('/favorites', methods=['GET', 'POST'])
def addUpdateFavorites():
  """ Adds/updates the client's favorites request to the favorites table """

  if ('user_id' not in session ):

    flash(MUST_BE_LOGGED_IN, "error")
    return redirect ('/login')

  if request.method == 'GET':
 
    favorites = Favorite.query.filter_by(user_id = session['user_id']).all()
    return render_template("/favorites.html", favorites = favorites)

  else: # A user is adding or editing a Favorite

    favId = request.json['favId']
    userId = session['user_id']
    videoId = request.json['id']
    title = request.json['title']
    artist = request.json['artist']
    song = request.json['song']
    notes = request.json['notes']
    vid_thumbnail = request.json['thumbnail']

    # Favorite already exist so need to update record (vs create a new favorite)
    if (favId):
      fav = Favorite.query.filter_by(video_id=videoId, user_id = session['user_id']).first()

      fav.video_title = title
      fav.artist_name = artist
      fav.song_title = song
      fav.notes = notes
      db.session.commit()

    else: # no favorite existed so we need to add fav to databse

      fav = Favorite(user_id = userId, thumbnail = vid_thumbnail, video_id = videoId, video_title = title, artist_name = artist, song_title = song, notes = notes)
      db.session.add(fav)
      db.session.commit()


    # Update session variables with data enetered on Favorit screen
    session['artist'] = request.json['artist']
    session['song'] = request.json['song']
    
    # Convert Database Ojbect to Python Object so it can be serialized 
    videoObj = Video_Detail(fav.video_id, fav.thumbnail, fav.video_title,  fav.artist_name, fav.song_title, fav.notes, fav.id, fav.user_id)

 
    return jsonify(videoObj.serialize())

@app.route('/favorites/<int:id>', methods=['DELETE'])
def deleteFavorite(id):
  """ This method is called when the user clicks on the Fav icon and then clicks
       the delete fav checkbox on the modal form. 
       Favorites functionality will require user to be logged in but we still need to protect
       against someone simply typing in a URL with an id.  """
 
  if 'user_id' not in session: 
    flash(MUST_BE_LOGGED_IN, "error")
    form = LoginForm()
    return redirect ('/login')
  
  fav = Favorite.query.get(id)
  db.session.delete(fav)
  db.session.commit()

  return jsonify("Favorite Deleted")


@app.route('/logout', methods=['POST'])
def logout_user():
  """ Logs the user out of app"""

  flash(f"{session['username'].capitalize()}, {LOGOUT_SUCCESSFUL}", "success")

  session.pop('user_id')
  session.pop('username')

  return redirect('/login')