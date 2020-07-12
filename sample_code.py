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

      