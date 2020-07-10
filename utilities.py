# Imports for Lyrics Scraping solution 
import re
import urllib.request  
from bs4 import BeautifulSoup

def get_lyrics(artist,song_title):
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
    return [char for char in word] 

class Video: 
  # def __init__(self, id, title, thumbnail, artist, song):
  def __init__(self, id, title, thumbnail):

    self.id = id
    self.title = title
    self.thumbnail = thumbnail
 

class Video_Detail:
  def __init__(self, id, title, thumbnail, artist, song, notes, fav_id):
    self.id = id
    self.title = title
    self.thumbnail = thumbnail
    self.artist = artist
    self.song = song
    self.notes = notes
    self.fav_id = fav_id
  

 
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