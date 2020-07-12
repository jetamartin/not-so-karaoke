# For parsing duration of videos 
from isodate import parse_duration

# For parsing coverting characters in video titles (e.g. &39 to ')
import html.parser as htmlparser
from utilities import *
import pickle


import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm
from constants import *
from models import db, connect_db, User, Favorite


app = Flask(__name__)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///nskdb'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
print("*********** H E L L O *****************")
# videos = []

@app.route('/', methods=['GET', 'POST'])
def index():
  form = SearchForm()
  if form.validate_on_submit():

    # Get values entered on Video Search screen
    artist = form.artist.data.strip()
    song = form.song.data.strip()

    ######## Note will need to replace this line once user SignIn is implementened..at login the user_id will be added to session
    session['user_id'] = 1;

    # Save search values as Session variables
    session['artist'] = artist
    # if user included song then save that in session
    if (song.strip()):
      session['song'] = song

    # Each time a new search is initiated remove prior search results from session
    if 'videos' in session: 
      session.pop('videos')

    # ENHANCEMENT NEEDED:  Need to check if there are results and if not need to display an appropriate message and return.
    search_results = search_for_matching_videos(artist, song)

    # REFACTOR CODE - Turn save video results in Video Object code below into a separate function
    # Save the YT video search results (video_id, title, thumbnail) and check to see if video is a current favor
    
    video_search_results = process_video_search_results (search_results, 'video_search')

    # My custom Video object is not serializable so pickle dump is used to serialize session variable before saving
    session['videos'] = pickle.dumps(video_search_results)
   

    return render_template('/search.html', form=form, videos = video_search_results)
  else:

    return render_template("/search.html", form=form)

# @app.route('/video/')
# def viewVideo():

@app.route('/video/<video_id>')
def viewVideo(video_id):
  # Pickle 'loads' method is used to 'un-serialize' video search results saved in session variable.
  videos = pickle.loads(session['videos'])
  
  # Call YT Video Detail API to retrieve JSON Data
  search_results = get_detailed_video_data(video_id)

  # ENHANCEMENT NEEDED:  Need to check if there are results and if not need to display an appropriate message and return.
  # Extract the detailed video information from the JSON Data returned from the YT API call 
  video = build_video_object(search_results, 'video_detail')

  # Get artist and Song entered on search form
  artist_input = session.get('artist', None)
  song_input = session.get('song', None)

  # Use search inputs plus heuristics to derive artist and song title (remember song_title is not required search input)
  artist_and_song_title = get_artist_and_song(artist_input, song_input, video.title)

  # Retrieve the lyrics
  lyrics = get_lyrics(artist_and_song_title['artist'], artist_and_song_title['song'] )

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


@app.route('/favorites', methods=['POST'])
def addUpdateFavorites():
  # import pdb; pdb.set_trace()
  userId = session['user_id']
  videoId = request.json['id']
  title = request.json['title']
  artist = request.json['artist']
  song = request.json['song']
  notes = request.json['notes']
  thumbnail = ""

  addFav = Favorite(user_id = userId, video_id = videoId, video_title = title, artist_name = artist, song_title = song, notes = notes)
  db.session.add(addFav)
  db.session.commit()
  # import pdb; pdb.set_trace()

  # Convert Database Ojbect to Python Object so it can be serialized 
  videoObj = Video_Detail(addFav.video_id, addFav.video_title, thumbnail, addFav.artist_name, addFav.song_title, addFav.notes, addFav.id, addFav.user_id )

  # import pdb; pdb.set_trace()
  # return jsonify({status: 'success', message: "Favorite successfully added to favorites list"})
  # return jsonify(video = [vid.serialize() for vid in videoObj])
  return jsonify(videoObj.serialize())

@app.route('/favorites/<int:id>', methods=['DELETE'])
def deleteFavorite(id):
  # import pdb; pdb.set_trace()
  fav = Favorite.query.get(id)

  db.session.delete(fav)
  db.session.commit()

  return jsonify("Favorite Deleted")

