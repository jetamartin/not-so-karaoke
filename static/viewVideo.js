// $(document).ready(function () {
      
      console.log("I'm in viewVideo.js file")
      videos = ['Z1RJmh_OqeA', 'EnJKHVEzHFw', '3mwFC4SHY-Y', 'mqhxxeeTbu0', 'OZ3K4fK9cAQ', 'asmvv8w8JY0', 'MwZwr5Tvyxo', 'zRwy8gtgJ1A']
      // videos = ['Z1RJmh_OqeA', 'EnJKHVEzHFw']
      var vidNum = 0;
      const nextVideoBtn = document.getElementById("next-video-btn")
      const priorVideoBtn = document.getElementById("prior-video-btn")
      const pauseVideoBtn = document.getElementById("pause-video-btn")
      const playVideoBtn = document.getElementById("play-video-btn")
      const stopVideoBtn = document.getElementById("stop-video-btn")
      const playerDiv = document.getElementById("player")
      const lyricsSearch = document.getElementById("lyrics-search-form")
      const favorites = document.getElementById("favorites")
      const vidDetailFavSubmit = document.getElementById("video-detail-fav-submit")
      const vidDetailDelFav = document.getElementById("video-detail-delete-fav")


      // nextVideoBtn.addEventListener("click", playNextVideo1);
      // priorVideoBtn.addEventListener("click", playPriorVideo);
      // pauseVideoBtn.addEventListener("click",pauseVideo);
      // playVideoBtn.addEventListener("click", playVideo);
      // stopVideoBtn.addEventListener("click", stopVideo)


      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;

      function onYouTubePlayerAPIReady() {
        player = new YT.Player('player', {
           // height: '390',
          // width: '640',
          // videoId: "dD-SpHH7qDA",
         
          // videoId: playerDiv.dataset.videoid,
          playerVars: { 'autoplay': 0, 'controls': 1, 'fs': 0},
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onError
          }
        });

        console.log(playerDiv.dataset.videoid)
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
    
        console.log("*****OnPlayerReady Function")
        // Play video that has been cued up above
        // event.target.playVideo();


        console.log('***** videoId', playerDiv.dataset.videoid)

        // Autoplays video
        // player.loadVideoById(playerDiv.dataset.videoid, 0)

        // Cues up the video...user must press play to play video
        player.cueVideoById(playerDiv.dataset.videoid)

        // Que up a list of videos from a list and play them       
        // player.loadPlaylist(videos)


        
        // let playerState = player.getPlayerState()
        // console.log('PlayerState', playerState)
        // if (playerState == 5) {


        //   event.target.playVideo();


        // }


        // lyricElementResize()
      }

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
      var done = false;
      function onPlayerStateChange(event) {
        // Allows me to retrive Title of video playing, id, etc. 
       
        // console.log(player.getVideoData()) 
        // if (event.data == YT.PlayerState.PLAYING && !done) {
        //   setTimeout(stopVideo, 6000);
        //   done = true;
        // } 

      }

      // function onPlayerStateChange(event) {        
      //   if(event.data === 0) {   
      //     alert("Video Finished"); 
      //     vidNum += 1;
      //     playNextVideo(vidNum)
      //   }
      // }

      function onError(event) {
        console.log("in onError function", event)
        console.log('Error message: ', event)

      }

      function stopVideo() {
        player.stopVideo();
        done = false;
        player.nextVideo();
        
        // vidNum += 1;
        // if (vidNum < videos.length) {
        //   done = false;
        //   playNextVideo(vidNum)
        // }
      }
   

      function playNextVideo(vidNum) {
        if (vidNum < videos.length ) {
          console.log("Video Id: ", videos[vidNum])
          console.log("Video Num", vidNum)
          player.loadVideoById(videos[vidNum])
        }
      }

      function stopVideo() {
        player.stopVideo()
      }
  
      function playVideo() {
        player.playVideo()
      }

      function pauseVideo() {
        player.pauseVideo()
      }

      function playNextVideo1 () {
        player.nextVideo()
      }

      function playPriorVideo () {
        player.previousVideo()
      }

      function lyricElementResize() {
        console.log("lyricElementResize() - Triggered ")
        var videoFrame = document.getElementById("player");
        var videoHeight = videoFrame.offsetHeight;
        console.log("*********videoHeight", videoHeight);
        var lyricFrame = document.getElementById("lyrics")
        lyricFrame.style.maxHeight = videoHeight + "px";
        
      }

      async function requestMoreLyrics(evt) {
        console.log("Process the submit Lyrics request form")
        evt.preventDefault()
        // const lyricsSearch = $("#lyrics-search-form")
        const inputArtistName = $("#artist").val()
        const inputSongTitle = $("#song").val()
        const lyricsSearchResults = $("#lyrics-search-results")
        params = {artist: inputArtistName, song: inputSongTitle}

        try {
          const res = await axios.post('http://localHost:5000/lyrics', params)    
          if (res.data) {
            $("#lyrics-content").html(res.data) 
          }
        } catch(err) {
          console.log("Error message")
        }
      }

      // $("#favorites").click(function(){
      //   console.log("Favorite was clicked")
      //   $(this).find('i').toggleClass('far fa-heart fas fa-heart')
      // });
      lyricsSearch.addEventListener("submit", requestMoreLyrics);


      favorites.addEventListener('click', function (evt) {
        // Values in Video Detail card
        videoDetailTitle = $("#video-detail-title").text()
        videoDetailArtist = $("#video-detail-artist").text()
        videoDetailSong =  $("#video-detail-song").text()
        videoDetailNotes =  $("#video-detail-notes").text()

        // Input fields of Favorite Video Save Modal form
        inputVideoTitle = $('#input-video-title')
        inputArtistName = $('#input-artist-name')
        inputSongTitle = $('#input-song-title')
        inputVideoNotes = $('#input-video-notes')


        console.log('Favorites was clicked')
        if ( event.target.className == 'far fa-heart' ) {   // Not currenty a favorite - Make it a favorite
          console.log("Heart clicked was outline")
          // Make it a favorite 
          // Generate modal for to save favorite
          $('#fav-save-modal').modal()
          inputVideoTitle.val(videoDetailTitle)
          inputArtistName.val(videoDetailArtist)
          inputSongTitle.val(videoDetailSong)
          inputVideoNotes.val(videoDetailNotes)
         

          console.log("Form is filled in")

          
          // Send a message ajax to server to save favorite in the database
          // if successful then 
          //  - generate a success message 
          //  - toggle heart to solid
          
        } else {  
          console.log("Heart clicked was solid heart")

          // Already a favorite...make it a non-favorite

          // Generate a modal window to confirm delete
          $("#fav-delete-modal").modal()
          // if user confirms un-favoriting then 
          //  - send an ajax message to server requesting deletion
          //  - if response indicates success then toggle class else generate error message
          // else close modal window

        }
        
      });

      vidDetailFavSubmit.addEventListener('click', addUpdateFavorites)

      async function addUpdateFavorites(evt) {
        console.log("Send detailed video info to server to add to favorites")
        const favSaveModal = $("#fav-save-modal")

        evt.preventDefault()
        // const lyricsSearch = $("#lyrics-search-form")
        const videoId = $("iframe").data('videoid')
        const inputVideoTitle = $("#input-video-title").val()
        const inputArtistName = $("#input-artist-name").val()
        const inputSongTitle =  $("#input-song-title").val()
        const inputVideoNotes =  $("#input-video-notes").val()

        params = {id: videoId, title: inputVideoTitle, artist: inputArtistName,  song: inputSongTitle, notes: inputVideoNotes}

        try {
          const res = await axios.post('/favorites', params)    
          if (res.data) {
            // $("#favorites").data('fav_id', res.data)
            $("#favorites").data('fav_id', res.data.fav_id)
            $('#video-detail-title').text(res.data.video_title)
            $("#video-detail-artist").text(res.data.artist_name)
            $("#video-detail-song").text(res.data.song_title)
            $("#video-detail-notes").text(res.data.video_notes)

            console.log("Favorite was added")
            $('#favorites i').toggleClass('far fa-heart fas fa-heart')
            // Show the notes
            $("#video-detail-notes-section").toggleClass('hide')
            favSaveModal.modal('hide')
          }
        } catch(err) {
          console.log("Error message")
        }
      }

      vidDetailDelFav.addEventListener('click', delFavorites)      

      async function delFavorites(evt) {

        const favDelModal = $("#fav-delete-modal")
        console.log("Function delFavorites")
        // Get the videoId from the details page
        videoId = $("iframe").data('videoid')
        userId = $("iframe").data('user_id')
        fav_id = $("#favorites").data('fav_id')

        try {
          const res = await axios.delete(`/favorites/${fav_id}`) 
          if (res.data) {
            console.log("Favorite was deleted")
            $('#favorites i').toggleClass('far fa-heart fas fa-heart')
            $("#favorites").data("fav_id", "")
            // $("#favorites").removeAttr("data-fav_id")
            // Hide the notes section
            $("#video-detail-notes-section").toggleClass('hide')
            favDelModal.modal('hide')
          }
        } catch(err) {
          console.log("Error message")
        }
      }
     // }); 