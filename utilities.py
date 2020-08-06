# Imports for Lyrics Scraping solution 
import re
import urllib.request  
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from flask import session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Favorite

import json

# For parsing coverting characters in video titles (e.g. &39 to ')
import html.parser as htmlparser

from constants import * 
import requests
from requests.exceptions import HTTPError
from flask import flash

class AppURLopener(urllib.request.FancyURLopener):
  # version = "Mozilla/5.0"
  version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'


def get_lyrics(artist,song_title):
  """ Scrapes the lyric data from azlyrics website """
  artist = artist.lower()
  song_title = song_title.lower()
  # remove all except alphanumeric characters from artist and song_title
  artist = re.sub('[^A-Za-z0-9]+', "", artist)
  song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
  # import pdb; pdb.set_trace()
  if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
      artist = artist[3:]

  url = LYRICS_URL+artist+"/"+song_title+".html"
  print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
  print(artist, song_title)
  print(url)
  print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')  

  try:
    # It appears the azLyricss is blocking attempts to scrape lyrics made by my app when running on Heroku server.
    # as the app works perfectly when the server is running on local host. 
    # I tried three different methods to get the lyrics from the AZlyrics website using my server app running on Heroku
    # but all of them apparently appear to have been blocked by the AZLyrics
    # website...returning a HTTP Status of 403 forbidden.

    # (1) Original method to read content from AZLyrics website
    # content = urllib.request.urlopen(url).read()
    # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

    request = urllib.request.Request(url, )
    content = urllib.request.urlopen(request).read()
    
    # (2) Second experiment reading content from AZLyrics
    #  Manually set a user agent to avoid server's web security (e.g., mod_security) that may be preventing scraping
    # see stackoverflow: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping 
    # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    # req = Request(url, headers=headers)
    # content = urlopen(req, timeout=10).read()

    # (3) Final option tried was reading content from URL using "request"
    # This last approach resulted in an "Exception occurred in retrieving lyrics: list index out of range" rather than a 403 status

    # content = requests.get(url, headers=headers).text
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    # content = requests.get(url, headers=headers)
    # print(content.request.headers)
    # content = content.text
    
    soup = BeautifulSoup(content, 'html.parser')
    lyrics = str(soup.encode("utf-8"))
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%% lyrics %%%%%%%%%%%%%%%%%%%%')
    print(lyrics)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%% lyrics %%%%%%%%%%%%%%%%%%%%')

    # lyrics lies between up_partition and down_partition
    up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
    down_partition = '<!-- MxM banner -->'
    lyrics = lyrics.split(up_partition)[1]
    # import pdb; pdb.set_trace()
    lyrics = lyrics.split(down_partition)[0]
    # import pdb; pdb.set_trace()
    lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip().replace('\\r', '').strip().replace('\\n', '').strip().replace('\\', '')
    return {'status':'success', 'msg': 'ok', 'lyrics': lyrics }
  except Exception as e:
    print(f"Exception occurred in retrieving lyrics: {str(e)}")
    return {'status': 'error', 'msg': 'Exception occurred \n' +str(e), 'lyrics': None}


class Video: 
  """ Creates an object with core video content """
  # def __init__(self, id, title, thumbnail, artist, song):
  def __init__(self, id, title, thumbnail, fav_id):

    self.id = id
    self.title = title
    self.thumbnail = thumbnail
    self.fav_id = fav_id
 

class Video_Detail:
  """ Creates and object with all the data needed for various views """
  def __init__(self, video_id, thumbnail, title, artist, song, notes, fav_id, user_id):
    self.id = video_id
    self.thumbnail = thumbnail
    self.title = title
    self.artist = artist
    self.song = song
    self.notes = notes
    self.fav_id = fav_id
    self.user_id = user_id

  def serialize(self):
    """ Serializes the data in the Video_Detail object so it can be sent as JSON data """
    return {
      'video_id': self.id,
      'thumbnail': self.thumbnail,
      'video_title': self.title,
      'artist_name':self.artist,
      'song_title': self.song,
      'video_notes':self.notes,
      'fav_id': self.fav_id,
      'user_id': self.user_id
    }

def split(word): 
  """ Takes a string and breaks it into array containing each of the letters of the string """
  return [char for char in word] 
 
# Use heuristics to extract artist and song title from video title
def extract_artist_song_from_video_title(title, artist_input, song_input):
  """ Extract the artist name and song title out of Video title """ 
  artist_song = []

  # Separate artist and song title from video title and return them in list (artist_song) 
  artist_song = separate_artist_song (title, artist_input)

  # Extract and cleanse artist name
  artist_title = extract_cleanse_artist(artist_song)

  # Extract and cleanse song_title
  song_title = extract_cleanse_song_title(artist_song)


  return {'artist_title': artist_title, 'song_title' : song_title}


def pick_final_artist_and_song_title(artist_song_title, artist_input, song_input):
  """ Picks the final version of artist name and song title to be used for lyrics search
      Note: Current algorithm gives priority to artist/song from video title vs relying solely on user search input because:
      - User may not enter the entire name of the band (e.g., "cranberries" vs "The Cranberries")
      - User may not enter a song title at all if they want to see all videos from a particular artist
      - User may not know the exact name of a song and the video title is more likely to contain the correct title
  """

  song = ""
  artist = ""
  artist_title = artist_song_title['artist_title']
  song_title = artist_song_title['song_title']

  # By default set artist to what user entered in the search form (artist_input) and then refine from there
  artist = artist_input

  # But if artist in artist title matches use artist in video title as that may be more complete and accurate
  if (artist_input.lower() in artist_title.lower()):
    artist = artist_title
  # If artist & song ordering in video title was reversed then un-reverse them in assignment
  elif (artist_input.lower() in song_title.lower() and artist_input.lower() not in artist_title.lower()):
    artist = song_title
    song = artist_title

  if (not song and not song_input):  
    # import pdb; pdb.set_trace()
    song = song_title
  elif (song_input): # If user entered song title on search form just use Song title they requested. 
    # import pdb; pdb.set_trace()
    song = song_input

  return {'artist' : artist, 'song' : song}


def extract_cleanse_song_title(artist_song):
  """ Extract clean song title name and return it. """
  print(artist_song)
  # import pdb; pdb.set_trace()

  # Song title raw is possible title from video plus other non-related title info (e.g., '(official video)')
  song_title_raw = artist_song[1].strip()
  song_words = song_title_raw.split(' ')

  song_title = ""

  # Remove extra/not song title related info text from Video Title (e.g. '(Official Video)')
  if song_title_raw != "":
    for song_word in song_words:
      song_letters = split(song_word)
    # Extraneous info is typically appended after the 'true' video title so when this extraneous info
    #  is detected all subsequent text in title is removed
      if song_letters[0].isalpha() or song_letters[0].isnumeric():
        song_title = song_title + f"{song_word} " 
      else:
        break  # ignore all text once extraneous/non-alpha text is first encountered in title

  song_title = song_title.strip()
  return song_title


def extract_cleanse_artist(artist_song):
  """ Extract clean artist name and return it """
  return artist_song[0].strip()

def no_delimeter_separation(title, artist_input):
  """ Separate Artist and Song from Video title if no delimeter present in video title """
  artist_song = []
  start_index = title.lower().find(artist_input.lower())
  end_index = start_index + len(artist_input.lower()) #Find ending position of artist name in title
  if (start_index != -1 ):  # Artist name is found in Video Title
    artist_song.append(title[start_index:end_index])  # Add everything up to and including the artist name in artist_song[0]
    artist_song.append(title[:start_index])  # Add everything after the artist name to artist_song[1]
    artist_song
  else:  # if Artist name was not found in the title  
    artist_song.append(artist_input)
    artist_song.append(title)
  artist_song
  # import pdb; pdb.set_trace()
  return artist_song


def separate_artist_song (title, artist_input):
  """ Separate Artist and Song from Video title by keying off of typical delimeter used in video titles. If no delimeter then 
      then use artist name entered in search to assist in extracting artist name.
    Returns a list containing separated artist and song title  """

  if '-' in title:
    artist_song = title.split('-')
  elif ':' in title:
    artist_song = title.split(':')
  elif '|' in title:
    artist_song = title.split('|')
  else: # No 'standard' delimiteer used in Video title to delineate song  to separate Artist from Song Title so use Artist name to separate Artist and Song title
    artist_song = no_delimeter_separation(title, artist_input)
  return artist_song

def get_video_info(result, search_type):
  """ Extract key video info from json data """

  # Parser is required to remove special characters (e.g., &#39) that are present in titles
  parser = htmlparser.HTMLParser()
  # import pdb; pdb.set_trace()
  video_title = parser.unescape(result['snippet']['title'])
  video_thumbnail = result['snippet']['thumbnails']['default']['url']

  # import pdb; pdb.set_trace()
  
  if (search_type == 'video_search'):
    video_id = result['id']['videoId']
  else: # 'video_detail'
    video_id = result['id']
  return {
    'video_id' : video_id,
    'video_title' : video_title,
    'video_thumbnail' : video_thumbnail,
  }

def build_video_object(json_video_info, search_type):
  """ Builds a video object from JSON search results and whether favorite exist for this user"""
  # import pdb; pdb.set_trace()
  # Extract video info from 
  video_info = get_video_info(json_video_info, search_type)


  # Check to see if video is in current user's favorites list...if so then return fav_id else return None
  fav_id = isFavoriteVideo(video_info['video_id'])
 

  # Create a video object for each video returned from the search..this will be used in the view template to display results
  video = Video(video_info['video_id'], video_info['video_title'], video_info['video_thumbnail'], fav_id )

  return video

  

def process_video_search_results (searchResults, search_type):
  """ Translate YT JSON video search results into a list of Video objects. Returns a list of resulting Video Objects  """
  videos = []
  for result in searchResults: 
  
    # Build video object for each video returned in json
    video = build_video_object(result, search_type)
    
    # Add video to list of video objects 
    videos.append(video)

  return videos

def isFavoriteVideo(video_id):
  """ Check database to see if video is in user's favorites list. Return id of favorite if found or return None """
  # import pdb; pdb.set_trace()
  fav_id = None;
  if 'user_id' in session:
    favResult = Favorite.query.filter_by(video_id=video_id, user_id = session['user_id']).first()
    if favResult:
      fav_id = favResult.id
    return fav_id


def get_detailed_video_data(video_id):
  """ Call YT API to retrieve detailed video information """
  # Currently I'm making a second call to YT Search to get video details..so session videos aren't really being used.
  video_params = {
    'key'          : YOUTUBE_API_KEY,
    # 'part'         : {'contentDetails', 'snippet', 'statistics', 'status'}, 
    'part'         : 'snippet',
    'maxResults'   : 9, 
    'id'           : video_id, 
    'type'         : 'video'
  }
  search_results = yt_api_call(YT_VIDEO_DETAIL_URL, video_params)
  return search_results


def get_artist_and_song(artist_input, song_input, title):
  """ Uses video title, search inputs and heuristics to get Artist name and song title
      The heuristics account for the fact that the user isn't required to enter song title
      as a search parameter and the user may not fill in the full artist name """
  # Extract artist and song title from video title
  artist_song_title = extract_artist_song_from_video_title(title, artist_input, song_input)

  # Determine final "version" of Artist and Song title to use in Lyrics search. Version could be values from
  # search form or from video title selected for view or a combination of both
  final_artist_and_song_title = pick_final_artist_and_song_title(artist_song_title, artist_input, song_input)

  return final_artist_and_song_title


def create_detail_video_object(video, artist_and_song_title):
  """ Builds a detailed video object inclusive of notes if present """ 
 
  vid_id = video.id
  vid_title = video.title
  vid_thumbnail = video.thumbnail
  vid_artist = artist_and_song_title['artist']
  vid_song = artist_and_song_title['song']
  favResult = None;
  if ('user_id' in session): 
    favResult = Favorite.query.filter_by(video_id=vid_id, user_id=session['user_id']).first()
  if favResult:
    fav_id = favResult.id
    vid_notes = favResult.notes
  else: 
    fav_id = "";
    vid_notes = "";

  video_details = Video_Detail(vid_id, vid_thumbnail, vid_title,  vid_artist, vid_song, vid_notes, fav_id, session.get('user_id'))
  return video_details

def build_list_of_video_objects(video_search_results):
  """ Builds a list of detailed video objects """ 
  video_details_objects_list = []
    # Get artist and Song entered on search form
  artist_input = session.get('artist', None)
  song_input = session.get('song', None)

  for video in video_search_results:

    # import pdb; pdb.set_trace()
    # Use search inputs plus heuristics to derive artist and song title (remember song_title is not required search input)
    artist_and_song_title = get_artist_and_song(artist_input, song_input, video.title)

    video_details_object = create_detail_video_object(video, artist_and_song_title)

    video_details_objects_list.append(video_details_object)
  return video_details_objects_list

def search_for_matching_videos(artist, song):
  """ Calls YT API to find matching videos based on user search criteria """

  videos = []
  search_params = {
    'key'          : YOUTUBE_API_KEY,
    'q'            : f" {artist} + {song}", 
    'part'         : 'snippet',
    'maxResults'   : 9, 
    'type'         : 'video'
  }
  results = ''
  search_results = yt_api_call(YT_VIDEO_SEARCH_URL, search_params)
  return search_results



def yt_api_call(yt_api, search_params):
  """ Calls appropriate API (Search or Detail) and handles any associated exceptions"""
  try:
     #  Issue request to YouTube SEARCH API to find matching videos
    req = requests.get(yt_api, params = search_params)
    req.raise_for_status()
  except requests.exceptions.HTTPError as http_err:
    print (f"Http Error: {http_err}")
    flash(f"Http Error: {http_err}")
    search_results = { 'status': 'error', 'msg': 'http_err', 'results': http_err }
  except requests.exceptions.ConnectionError as connect_err:
    print (f"Error Connecting: {connect_err}")
    flash(f"Connection Error: Unable to establish network connection. Check your network connection. ")
    search_results = { 'status': 'error', 'msg': 'connect_err', 'results': connect_err }
  except requests.exceptions.Timeout as timeout_err:
    print (f"Timeout Error: {timeout_err}")
    flash(f"Timeout Error: {timeout_err}")
    search_results = { 'status': 'error', 'msg': 'timeout_err', 'results': timeout_err }
  except requests.exceptions.RequestException as general_err:
    print (f"General Error: {general_err}")
    flash(f"General Error: {general_err}")
    search_results = { 'status': 'error', 'msg': 'timeout_err', 'results': general_err }
  else:
    if yt_api == YT_VIDEO_SEARCH_URL:
      #  Get results from YT Video search 
      search_results = { 'status': 'success', 'msg': 'ok', 'results': req.json()['items'] }
    else:  # YT_VIDEO_DETAIL_URL
      search_results = { 'status': 'success', 'msg': 'ok', 'results': req.json()['items'][0] }
  finally:
    return search_results
  