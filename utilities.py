# Imports for Lyrics Scraping solution 
import re
import urllib.request  
from bs4 import BeautifulSoup

from flask import session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Favorite

# For parsing coverting characters in video titles (e.g. &39 to ')
import html.parser as htmlparser

from constants import * 
import requests

def get_lyrics(artist,song_title):
  """ Scrapes the lyric data from azlyrics website """
  artist = artist.lower()
  song_title = song_title.lower()
  # remove all except alphanumeric characters from artist and song_title
  artist = re.sub('[^A-Za-z0-9]+', "", artist)
  song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
  if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
      artist = artist[3:]
  url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
  
  try:
      content = urllib.request.urlopen(url).read()
      soup = BeautifulSoup(content, 'html.parser')
      lyrics = str(soup)
      # lyrics lies between up_partition and down_partition
      up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
      down_partition = '<!-- MxM banner -->'
      lyrics = lyrics.split(up_partition)[1]
      lyrics = lyrics.split(down_partition)[0]
      lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()
      return lyrics
  except Exception as e:
      return "Exception occurred \n" +str(e)


def split(word): 
  """ Takes a string and breaks it into array containing each of the letters of the string """
  return [char for char in word] 

class Video: 
  """ Creates an object with core video content """
  # def __init__(self, id, title, thumbnail, artist, song):
  def __init__(self, id, title, thumbnail, fav_id):

    self.id = id
    self.title = title
    self.thumbnail = thumbnail
    self.fav_id = fav_id
 

class Video_Detail:
  """ Creates and object with all the data needed on the Video Detail screen """
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
      - User may not enter the entire name of the band (e.g., cranberries vs The Cranberries)
      - User may not enter a song title at all if they want to see all videos from a particular artist
      - User may not know the exact name of a song and the video title is more likely to be correct. 
      
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

  # Song title raw is possible title from video plus other non-related title info (e.g., '(official video)')
  song_title_raw = artist_song[1].strip()
  song_words = song_title_raw.split(' ')

  song_title = ""

  # Remove extra/not song title related info text from Video Title (e.g. '(Official Video)')

  for song_word in song_words:
    song_letters = split(song_word)

  # Extraneous info is typically appended after the 'true' video title so when this extraneous info
  #  is detected all subsequent text in title is removed
    if song_letters[0].isalpha():
      song_title = song_title + f"{song_word} " 
    else:
      break  # ignore all text once extraneous/non-alpha text is first encountered in title

  song_title = song_title.strip()
  return song_title


def extract_cleanse_artist(artist_song):
  """ Extract clean artist name and return it """
  return artist_song[0].strip()

def no_delimeter_separation(artist_input):
  """ Separate Artist and Song from Video title if no delimeter present in video title """
  start_index = title.lower().find(artist_input.lower())
  end_index = start_index + len(artist_input.lower()) #Find ending position of artist name in title
  if (start_index != -1 ):  # Artist name is found in Video Title
    artist_song.append(title[:end_index])  # Add everything up to and including the artist name in artist_song[0]
    artist_song.append(title[end_index:])  # Add everything after the artist name to artist_song[1]
  else:  # if Artist name was not found in the title  
    artist_song.append(artist_input)
    artist_song.append(title)
  return artist_song


def separate_artist_song (title, artist_input):
  """ Separate Artist and Song from Video title by keying off of typical delimeter used in video titles. If no delimeter then 
      then use artist name entered in search to assist in extracting artist name.
    Returns a list containing separated artist and song title  """

  if '-' in title:
      artist_song = title.split('-')
  elif ':' in title:
      artist_song = title.split(':')
  else: # No 'standard' delimiteer used in Video title to delineate song  to separate Artist from Song Title so use Artist name to separate Artist and Song title
    no_delimeter_separation(title, artist_input)

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

  # import pdb; pdb.set_trace() 

  
  # Check to see if video is in current user's favorites list...if so then return fav_id else return None
  fav_id = isFavoriteVideo(video_info['video_id'])
 

  # Create a video object for each video returned from the search..this will be used in the view template to display results
  video = Video(video_info['video_id'], video_info['video_title'], video_info['video_thumbnail'], fav_id )

  return video

  

def process_video_search_results (searchResults, search_type):
  """ Translate YT JSON video search results into a list of Video objects. Returns a list of resulting Video Objects  """
  videos = []
  for result in searchResults: 
    # import pdb; pdb.set_trace()
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
      print(f'================================> video_id: {video_id} fav_id = {fav_id}' )
  return fav_id


def get_detailed_video_data(video_id):
  """ Call YT API to retrieve detailed video information """
  # Currently I'm making a second call to YT Search to get video details..so session videos aren't really being used.
  video_params = {
    'key'          : YOUTUBE_API_KEY,
    # 'part'         : {'contentDetails', 'snippet', 'statistics', 'status'}, 
    'part'         : 'snippet',
    'maxResults'   : 15, 
    'id'           : video_id, 
    'type'         : 'video'
  }

  # ENHANCEMENT NEEDED:  Need to check if there are results and if not need to display an appropriate message and return.
  # Get results of YT Video Detail search.   
  search_results = requests.get(YT_VIDEO_DETAIL_URL, params = video_params) 
  video_json_info = search_results.json()['items']

  return video_json_info[0]

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
    fav_id = None;
    vid_notes = None;

  video_details = Video_Detail(vid_id, vid_thumbnail, vid_title,  vid_artist, vid_song, vid_notes, fav_id, session.get('user_id'))
  return video_details


def search_for_matching_videos(artist, song):
  """ Calls YT API to find matching videos based on user search criteria """

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


  #  Get results from YT Video search 
  search_results = req.json()['items']

  return search_results