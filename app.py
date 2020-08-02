# For parsing duration of videos 
from isodate import parse_duration

# For parsing coverting characters in video titles (e.g. &39 to ')
import html.parser as htmlparser
from utilities import *
import pickle
from sqlalchemy import exc


import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm, SignupForm, LoginForm
from constants import *
from models import db, connect_db, User, Favorite
from secrets import API_SECRET_KEY


app = Flask(__name__)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///nskdb'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.config.update(SESSION_COOKIE_SAMESITE='Lax')
toolbar = DebugToolbarExtension(app)

connect_db(app)
print("*********** H E L L O *****************")
# videos = []

@app.route('/')
def home():
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
      flash("User account is already taken. If this is your account you'll need to login.", "error")
      return render_template("/signup.html", form=form)
    else: 
      session["user_id"] = user.id
      session["username"] = user.username
      flash(f"Welcome {user.username}! Your new account has been created and you've been logged in!", "success")
      return redirect("/search")

  else:
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
        flash(f"Welcome back {user.username}! You're now logged in!", "success")
        session["user_id"] = user.id # keep logged in
        session["username"] = user.username
        return redirect("/search")
      else:
        form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route('/search', methods=['GET', 'POST'])
def index():
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

    # **** No need to store or manipulate videos returned from search in a sessin variable
    # Each time a new search is initiated remove prior search results from session
    # if 'videos' in session: 
    #   session.pop('videos')
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
        flash('Sorry no videos matching your search criteria were found...check your search criteria and try another search', "error")
        return redirect('/search')


      # Save the YT video search results (video_id, title, thumbnail) and check to see if video is a current favor
      video_search_results = process_video_search_results (json_results, 'video_search')

      # Get artist and Song entered on search form
      artist_input = session.get('artist', None)
      song_input = session.get('song', None)

      # For each video in video_search_results build a list of video_detail_objects 
      video_detail_objects_list = build_list_of_video_objects(video_search_results)

      return render_template('/search.html', form=form, videos = video_detail_objects_list)

  else:

    return render_template("/search.html", form=form)


@app.route('/video/<video_id>')
def viewVideo(video_id):

    # ***** No need store search results in session variable if I make another call to YT API below
  # Pickle 'loads' method is used to 'un-serialize' video search results saved in session variable.
  # videos = pickle.loads(session['videos'])
  
  # Call YT Video Detail API to retrieve JSON Data
  search_results = get_detailed_video_data(video_id)
 
  if (search_results['status'] == 'error'):
    return redirect('/search')
  else: # YT API returned success status code
    json_results = search_results['results']
    # if api request was successful but no videos found matching search criteria then notify user
    if len(json_results) == 0:
      flash('Sorry no videos matching your search criteria were found...check your search criteria and try another search', "error")
      return redirect('/search')

  # ENHANCEMENT NEEDED:  Need to check if there are results and if not need to display an appropriate message and return.
  # Extract the detailed video information from the JSON Data returned from the YT API call 
  video = build_video_object(search_results['results'], 'video_detail')

  # Get artist and Song entered on search form
  artist_input = session.get('artist', None)
  song_input = session.get('song', None)

  # Use search inputs plus heuristics to derive artist and song title (remember song_title is not required search input)
  artist_and_song_title = get_artist_and_song(artist_input, song_input, video.title)

  # Retrieve the lyrics
  lyrics = get_lyrics(artist_and_song_title['artist'], artist_and_song_title['song'] )
  # import pdb; pdb.set_trace()

  # Build a detail video object to simplify passing data into view
  video_details = create_detail_video_object(video, artist_and_song_title)

  # Don't think I need to save this in session variable
  session['videoDetails'] = pickle.dumps(video_details)

  return render_template('/view-video.html', video_details = video_details, lyrics = lyrics)


@app.route('/lyrics', methods=['POST'])
def getMoreLyrics():
  artist = request.json['artist']
  song = request.json['song']
  lyrics = get_lyrics(artist, song)
  return jsonify(lyrics)


@app.route('/favorites', methods=['GET', 'POST'])
def addUpdateFavorites():
  if ('user_id' not in session ): 
    flash("This action is not allowed if you aren't logged in. Please login or signup to create an account", "error")
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
    flash("This action is not allowed if you aren't logged in. Please login or signup to create an account", "error")
    form = LoginForm()
    return redirect ('/login')
  # return render ('/login', form=form)
  
  fav = Favorite.query.get(id)
  db.session.delete(fav)
  db.session.commit()

  return jsonify("Favorite Deleted")


# NOTE: This should be implemented as a POST route rather than GET route
# In navigation bar either include a blank form to send post or implement with JS
@app.route('/logout', methods=['POST'])
def logout_user():
  session.pop('user_id')
  session.pop('username')
  flash("So long for now..you've been logged out", "success")
  return redirect('/login')

@app.route('/about')
def about_page():
  return render_template("/about.html")