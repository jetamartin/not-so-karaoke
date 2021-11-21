# import lyricsgenius
from lyricsgenius import Genius
from constants import * 

def get_lyrics(artist,song_title):
  
  """ Retrieves lyrics from Genius.com using a python """
  artist = artist.lower()
  song_title = song_title.lower()

  genius = Genius(LYRICS_SECRET_KEY)

  # genius = lyricsgenius.Genius(LYRICS_SECRET_KEY)
 
  try:
    # import pdb; pdb.set_trace()
    song = genius.search_song(song_title, artist)
    # song = genius.song(song_title, artist)
    if (song):

      lyrics = song.lyrics.replace('\n', '<br>')
      return {'status':'success', 'msg': 'ok', 'lyrics': lyrics }

    else: # No matching lyrics were found
      status = 'error'
      msg = NO_MATCHING_LYRICS
      lyrics = None
      return {'status': status, 'msg': msg, 'lyrics': lyrics }

  except Exception as e:  
    print(f"Exception occurred in retrieving lyrics: {str(e)}")
    status = 'error'
    lyrics = None
    if e.status == 404:
      msg = f"{NO_MATCHING_LYRICS} (error-code ={e.status})"
    elif e.status == 403:
      msg = f"{LYRICS_SERVICE_NOT_RESPONDiNG} (error code={e.status}) "
    elif e.status == 500:

      msg = f"Server error occurred (error-code={e.status})"
    else: # Catch all for all other errors
      msg = f"{MISC_SERVER_ERROR} (error-code={e.status})"
      
    # import pdb; pdb.set_trace()
    return {'status': status, 'msg': msg, 'lyrics': lyrics}