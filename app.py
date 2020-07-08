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


from models import db, connect_db

CURR_USER_KEY = "curr_user"
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YT_VIDEO_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
YT_VIDEO_DETAIL_URL = 'https://www.googleapis.com/youtube/v3/videos'

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

    # import pdb; pdb.set_trace()
    artist = form.artist.data
    song = form.song.data

    session['artist'] = artist.strip()
    # if user included song then save that in session
    if (song.strip()):
      session['song'] = song.strip()

    # Each time a new search is initiated remove prior search results from session
    if 'videos' in session: 
      session.pop('videos')

    videos = []
    search_params = {
      'key'          : YOUTUBE_API_KEY,
      'q'            : f" {artist} + {song}", 
      'part'         : 'snippet',
      'maxResults'   : 15, 
      'type'         : 'video'
    }
    results = ''
    req = requests.get(YT_VIDEO_SEARCH_URL, params = search_params)

    results = req.json()['items']

    # print(results[5]['snippet']['title'])
    # print(results[8])
    # print(results)
    # import pdb; pdb.set_trace()

 
    video_ids = []
    video_titles = []

    # parser = htmlparser.HTMLParser()
    # for result in results: 
    #   video_ids.append(result['id']['videoId'])
    #   video_titles.append(result['snippet']['title'])

    # parser = htmlparser.HTMLParser()
    
    for result in results: 
      video_id = result['id']['videoId']
      video_title = result['snippet']['title']
      video_thumbnail = result['snippet']['thumbnails']['default']['url']
      video = Video(video_id, video_title, video_thumbnail)
      videos.append(video)

    session['videos'] = pickle.dumps(videos)
   
     # print(video_ids)
    # # print(video_titles)

    # parser = htmlparser.HTMLParser()
    # for video in videos:
    #   print(video.id)
    #   # print(parser.unescape(video.title))

    # video_params = {
    #   'key'          : YOUTUBE_API_KEY,
    #   'part'         : 'contentDetails, snippet, statistics, status', 
    #   'maxResults'   : 15, 
    #   # 'id'           : ','.join(video_ids), 
    #   'id'           : 'OMD8hBsA-RI', 
    #   'type'         : 'video'
    # }
      
    # vid_req = requests.get(video_url, params = video_params)
    # vid_results = vid_req.json()['items']

    # print(vid_req.text)
    # print(vid_results)


    # mins = int(parse_duration(vid_results[0]['contentDetails']['duration']).total_seconds()//60)
    # views = vid_results[0]['statistics']['viewCount']

    # # import pdb; pdb.set_trace()

      
    return render_template('/search.html', form=form, videos = videos)
  else:

    return render_template("/search.html", form=form)

# @app.route('/video/')
# def viewVideo():

@app.route('/video/<video_id>')
def viewVideo(video_id):
  videos = pickle.loads(session['videos'])
  title =''
  vid = ''  

  video_params = {
    'key'          : YOUTUBE_API_KEY,
    # 'part'         : {'contentDetails', 'snippet', 'statistics', 'status'}, 
    'part'         : 'snippet',
    'maxResults'   : 15, 
    'id'           : video_id, 
    'type'         : 'video'
  }
  
  vid_req = requests.get(YT_VIDEO_DETAIL_URL, params = video_params) 
  # import pdb; pdb.set_trace()
  vid_results = vid_req.json()['items']


  print(title)

  # import pdb; pdb.set_trace()
  # Search through list of video objects to locate video object with matching video id

  # ^^^^^^^^^^^^^^ Uncomment below
  # for video in videos:
  #   if video.id == video_id:
  #     vid = video
  #     break
  # ^^^^^^^^^^^^^^ Uncomment above

    
  # import pdb; pdb.set_trace()
  # Use parser to convert HTML representations of special characters to normal characters (e.g., &#39 is an apostrophe character) 
  # For example:  title for Journey's "Don't Stop Believin'"" would read "Don&#39;t Stop Believin&#39"
  parser = htmlparser.HTMLParser()

  # ^^^^^^^^^^^^^^ Uncomment below
  # title = parser.unescape(vid.title)
  # ^^^^^^^^^^^^^^ Uncomment above

  # *************Delete Line below ***********************
  title =  "Journey - Faithfully (Official Video)"
  # ************************************
  
  # Get artist and Song entered on search form

  # ^^^^^^^^^^^^^^ Uncomment below
  # artist_input = session.get('artist', None)
  # song_input = session.get('song', None)
  # ^^^^^^^^^^^^^^ Uncomment above
  # *************Delete Line below ***********************
  artist_input = 'Journey'
  song_input = None
  # ************************************



  # import pdb; pdb.set_trace()
  # Extract artist and song title from video title
  artist_song_title = extract_artist_song_from_video_title(title, artist_input, song_input)
  # import pdb; pdb.set_trace()

  # Determine final "version" of Artist and Song title to use in Lyrics search. Version could be values from
  # search form or from video title selected for view or a combination of both
  final_artist_and_song_title = pick_final_artist_and_song_title(artist_song_title, artist_input, song_input)

  # import pdb; pdb.set_trace()

  #  Get lyrics 
  lyrics = get_lyrics(final_artist_and_song_title['artist'], final_artist_and_song_title['song'])


# ^^^^^^^^^^^^^^ Uncomment below

  # create video detail object  
  # vid_id = video_id
  # vid_title = vid_results[0]['snippet']['title']
  # vid_thumbnail = vid_results[0]['snippet']['thumbnails']['default']['url']
  # vid_artist = final_artist_and_song_title['artist']
  # vid_song = final_artist_and_song_title['song']
  # vid_notes = ""
  # vid_fav = False
  # ^^^^^^^^^^^^^^ Uncomment above

# *************Delete Lines below ***********************
  vid_id = "OMD8hBsA-RI"
  vid_title = "Journey - Faithfully (Official Video)"
  vid_thumbnail = ""
  vid_artist = final_artist_and_song_title['artist']
  vid_song = final_artist_and_song_title['song']
  vid_notes = ""
  vid_fav = True
# *************Delete Lines above ***********************

  
  
  video_details = Video_Detail(vid_id, vid_title, vid_thumbnail, vid_artist, vid_song, vid_notes, vid_fav)

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
  import pdb; pdb.set_trace()
  title = request.json['title']
  artist = request.json['artist']
  song = request.json['song']
  notes = request.json['notes']

  # return jsonify({status: 'success', message: "Favorite successfully added to favorites list"})
  return jsonify("Favorite successfully added to favorites list")

  # @app.route('/favorites/<int:id>', methods=['DELETE'])
  @app.route('/favorites/del', methods=['POST'])
  def deleteFavorite():
    import pdb; pdb.set_trace()

    return jsonify("Favorite Deleted")

