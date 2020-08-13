# Check out  [Almost-Karaoke](https://almost-karaoke.herokuapp.com/)![](/static/AK_logo_v2_48x48.png "Almost Karaoke Logo")  running on Heroku 

**What is Almost-Karaoke?**  
-	Almost-karaoke is an easy to use web app that gives the user the ability to view a YouTube music video and the song’s lyrics side by side on the same web page.  
- Almost-Karaoke “marries” the world of YouTube video content with the massive lyrical database of Genius.com in a fun and easy way.  If you could represent Almost-Karaoke with a math formula it would be: **YouTube + Lyrics = Fun2**


**Why is it called Almost-Karaoke?** 
-	As we know “True Karaoke” players generally play the song without the primary vocals and with the lyrics displayed on or below the screen in sync with the music. 
-	“Almost-Karaoke” displays the actual music video (all vocals included) and the lyrics adjacent to the videow. Lyrics are not marked/synchronized or notated (in this release) in any way to match the music video.  

**How to use Almost-Karaoke?** (4 simple steps)
1.	Navigate to https://almost-karaoke.herokuapp.com/

2.	Enter your music video search criteria (i.e., artist name & optionally a song title) on the search page and click the search button. (This retrieves a list of matching YouTube videos);

3.	Select one of the videos from the search results by clicking on that video’s View button. 
(This will retrieve the selected YouTube video and matching lyrics and display them);

4.	 If you want to play the Video then just click on the Video’s Play button and it will start to play on that page   

•	*Note: More advanced features (e.g., favorites and more in the future) are/will be available if you register… and did I mention that's it's free to register.*


**Who would use Almost-Karaoke?**

There are probably many possible uses for this app but the ones that came to mind when I was building this app were: 
-	Someone wanting to learn/understand the lyrics of a “new” song and they want to watch/listen to the video while viewing the lyrics; 
-	Someone who enjoys singing along to YouTube Videos but they don’t have the lyrics committed to memory…yet.
-	Someone wanting to inject a little fun to their party by adding an Almost-Karaoke video sing-off competition for  the entertainment
-	And many more……
---
## Now for the Geeky stuff:
**What technologies were used to build Almost-Karaoke?**
-	The Server is written in Python using the Flask Framework with PostgreSQL as the backend database;
-	The Client is written using Javascript;
-	And of course HTML and CSS is used for display and styling of the content
-	External API’s (issued from the server)
     - Google YouTube API
     - Genius.com API via a Python library

**As a developer how would I install and run this code locally on my machine?**
1.	Install all of the pre-requisites on your local system:
    1.	Python
    2.	PostgreSQL 
2.	Clone the Git repository on your system;
3.	Create your own API keys for YouTube (video source) and Genius.com (lyrics source);
4.	Create a .env file in the root directory of the application with the following two variables defined:
     1. YOUTUBE_API_KEY= “insert your YouTube api key here"  
     2. LYRICS_SECRET_KEY = “insert your Genius.com api key here”
      - You’ll need to get your own YouTube and Genius.com keys. Directions for getting your own keys can be found here:
          - YouTube Key Directions:  https://developers.google.com/youtube/v3/getting-started
          -	Genus.com Key Directions:  https://genius.com/developers
3.	While in the root directory where you installed the app: 
    - Install the prerequisite python packages used by this app (as noted in requirements.txt file) by running the following command from the command line: **‘pip install -r requirements.txt’** 
4.	Create the Almost-Karaoke database using the following commands:
    - Run **‘psql’** from the command line (this will give you a PostgreSQL command line) and you should see **‘#psql:** ‘ as the command prompt; 
    -	Now run the following command to create the database: **‘createdb nskdb’** 
    -	Now exit psql by typing **‘\q’**
5.	Now From the project root directory create the necessary PostgreSQL tables by running the seed.py file via the command line: **‘python seed.py’** 
6.	Finally, to start up the application on your local machine you’ll need to:
    -	Run the  command: **‘flask run’** from the root directory; and
    -	From the browser type: **‘localhost: 5000** 
7.	At this point you should see the homepage of the Almost-Karaoke in your browser tab. 
