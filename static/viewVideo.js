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


        console.log('***** videoId', playerDiv.dataset.videoId)

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
        console.log('Favorites was clicked')
        if ( $('i').hasClass('far') ) {   // Not currenty a favorite

          console.log("Has far-fa-heart - outline heart ")
          // Make it a favorite 

          // Send a message ajax to server to save favorite in the database
          // if successful then 
          //  - generate a success message 
          //  - toggle heart to solid
          
        } else {  
          console.log("Has fas-fa-heart - solid heart ")

          // Already a favorite...make it a non-favorite

          // Generate a modal window to confirm delete
          $('#exampleModal').modal()
          // if user confirms un-favoriting then 
          //  - send an ajax message to server requesting deletion
          //  - if response indicates success then toggle class else generate error message
          // else close modal window

        }

        $('i').toggleClass('far fa-heart fas fa-heart')





        // if (event.target.className == "far fa-heart") {
        //   console.log('Clicked Heart outline')
        //   favorites.className = "fas fa-heart";
        //   // favorites.classList.remove('far');
        //   // favorites.classList.add('fas');
        // } else {  // Heart clicked was a solid heart
        //   console.log("Clicked Solid heart")
        //   favorites.className = "far fa-heart";

        //   // favorites.classList.remove('fas');
        //   // favorites.classList.add('far');
        // }

        
      });
    // }); 