# ------------------------------------------------------------------------------------------
# Example of using video details search to get info from different elements including 'statistics', 'status'
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
# ------------------------------------------------------------------------------------------

  # ------------------------------------------------------------------------------------------
  # ALTERNATIVE: If no more detail info is required from API then I could just use data from initial YT search
  # that is stored in session variable. Logic below find matching search results
  # ------------------------------------------------------------------------------------------

  # Search through list of video objects to locate video object with matching video id
  # ^^^^^^^^^^^^^^ Uncomment below
  # for video in videos:
  #   if video.id == video_id:
  #     vid = video
  #     break

  # Use parser to convert HTML representations of special characters to normal characters (e.g., &#39 is an apostrophe character) 
  # For example:  title for Journey's "Don't Stop Believin'"" would read "Don&#39;t Stop Believin&#39"
  # parser = htmlparser.HTMLParser()
  # title = parser.unescape(vid.title)
  # ----------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# Original Scraping code I used:
# Code below is code I used originally when scraping lyrics from AZlyrics website.
# This code includes several ways to scrape and access the lyrics. They all worked on local
# host but I always received a 403 from AZlyrics when I did this from Heroku. I suspect that
# azLyrics has implemented techniquest to apps on Heroku from scrapng their site. After spending 
# days and multiple ways to avoid the 403 I gave up and went with a lyricsgenius library that 
# i found on gitHub...so far it works. 
# 
# -------------------------------------START OF CODE -----------------------------------------------------------
# AppURLopener class - is used with one of the methods noted below to scrape website.
# class AppURLopener(urllib.request.FancyURLopener):
#   # version = "Mozilla/5.0"
#   version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

  # remove all except alphanumeric characters from artist and song_title
  # artist = re.sub('[^A-Za-z0-9]+', "", artist)
  # song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
  # import pdb; pdb.set_trace()
  # if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
  #     artist = artist[3:]

  # url = LYRICS_URL+artist+"/"+song_title+".html"

    # It appears the azLyricss is blocking attempts to scrape lyrics made by my app when running on Heroku server.
    # as the app works perfectly when the server is running on local host. 
    # I tried three different methods to get the lyrics from the AZlyrics website using my server app running on Heroku
    # but all of them apparently appear to have been blocked by the AZLyrics
    # website...returning a HTTP Status of 403 forbidden.

    # (1) Original method to read content from AZLyrics website
    # content = urllib.request.urlopen(url).read()

    
    # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    # headers={'user-agent': 'Mozilla/5.0'}
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    # request = urllib.request.Request(url, headers=headers)
    # content = urllib.request.urlopen(request).read()
    
    # (2) Second experiment reading content from AZLyrics
    #  Manually set a user agent to avoid server's web security (e.g., mod_security) that may be preventing scraping
    # see stackoverflow: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping 
    # headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    # req = Request(url, headers=headers)
    # content = urlopen(req, timeout=10).read()

    # (3) Third option tried was reading content from URL using "request"
    # This last approach resulted in an "Exception occurred in retrieving lyrics: list index out of range" rather than a 403 status

    # content = requests.get(url, headers=headers).text
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    # content = requests.get(url, headers=headers)
    # print(content.request.headers)
    # content = content.text

##############################################################################################################  # 
    # soup = BeautifulSoup(content, 'html.parser')
    # lyrics = str(soup.encode("utf-8"))


    # lyrics lies between up_partition and down_partition
    # up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
    # down_partition = '<!-- MxM banner -->'
    # lyrics = lyrics.split(up_partition)[1]
    # lyrics = lyrics.split(down_partition)[0]
    # lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip().replace('\\r', '').strip().replace('\\n', '').strip().replace('\\', '')
    # return {'status':'success', 'msg': 'ok', 'lyrics': lyrics }
# -------------------------------------END OF CODE -----------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------
# Code below was put in place to monitor all incoming and outgoing headers for debugging purposes
# ------------------------------------------------------------------------------------------------------------

# Enabling debugging at http.client level (requests->urllib3->http.client)
# you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# the only thing missing will be the response.body which is not logged.
# -------------------------------------START OF CODE -----------------------------------------------------------
# try: # for Python 3
#     from http.client import HTTPConnection
# except ImportError:
#     from httplib import HTTPConnection
# HTTPConnection.debuglevel = 1

# logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# requests.get('https://httpbin.org/headers')
# -------------------------------------END OF CODE -----------------------------------------------------------

