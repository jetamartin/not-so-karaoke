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
const favSaveModal = $("#fav-save-modal")
const delFav = $('#del-fav')



// $(document).ready(function () {
      
      console.log("I'm in viewVideo.js file")

      // var vidNum = 0;
      // const nextVideoBtn = document.getElementById("next-video-btn")
      // const priorVideoBtn = document.getElementById("prior-video-btn")
      // const pauseVideoBtn = document.getElementById("pause-video-btn")
      // const playVideoBtn = document.getElementById("play-video-btn")
      // const stopVideoBtn = document.getElementById("stop-video-btn")
      // const playerDiv = document.getElementById("player")
      // const lyricsSearch = document.getElementById("lyrics-search-form")
      // const favorites = document.getElementById("favorites")


      // const vidDetailFavSubmit = document.getElementById("video-detail-fav-submit")
      // const vidDetailDelFav = document.getElementById("video-detail-delete-fav")
      // const favSaveModal = $("#fav-save-modal")
      // const delFav = $('#del-fav')




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


      favorites.addEventListener('click', launchFavoritesModal);
      
      function launchFavoritesModal (evt) {
        // Determines which favorite's modal window to launch (add-favorite or remove-favorite) and launches it. 
        // Scenario 1: A heart outline (far fa-heart) denotes that the current video is not currently a favorite but the user 
        // wants to make it a fav;
        // Scenario 2: A solid red heart (fas fa-heart) indicates the video is already a favorite and clicking on it means the user wants
        // to remove it as one of their favorite;

        // Get the values from the video detail card to populate the 'Add to favorites' modal form.
        videoDetailTitle = $("#video-detail-title").text()
        videoDetailArtist = $("#video-detail-artist").text()
        videoDetailSong =  $("#video-detail-song").text()
        videoDetailNotes =  $("#video-detail-notes").text()

        // Get handle for input fields on the favorite modal
        inputVideoTitle = $('#input-video-title')
        inputArtistName = $('#input-artist-name')
        inputSongTitle = $('#input-song-title')
        inputVideoNotes = $('#input-video-notes')

        // Now populate the Add-to-Favorites modal with the data from the video detail card
        inputVideoTitle.val(videoDetailTitle)
        inputArtistName.val(videoDetailArtist)
        inputSongTitle.val(videoDetailSong)
        inputVideoNotes.val(videoDetailNotes) 

        // Display the populated Add Favorite modal screen
        $('#fav-save-modal').modal()

        // Scenario 1:  Current video is not a favorite
        if ( event.target.className == 'far fa-heart' ) { 
          inputVideoNotes.val("") 
          // Hide the delete check box because this video isn't a favorite yet 
          $('#fav-del-checkbox').addClass('hide')
        
        } else {  // Current video is already a fav and user wants to remove it as a favorite video

          // Display the Delete checkbox by removing 'hide' class
          $('#fav-del-checkbox').removeClass('hide')
        }
      }


     delFav.on( "click", function() {
        $('#del-fav-warning').toggleClass('hide')
      });

      vidDetailFavSubmit.addEventListener('click', processFavModalSubmit)

      async function processFavModalSubmit(evt) {
        // Process the User's submission of the Favorites Modal Form. Submitting the form could result in 3 different outcomes.
        // 1 - The video was not previously a Favorite and the User wishes add it to their favorites list 
        // 2 - The video was previously a Favorite but they want to edit fields (e.g., notes) of this existing favorite
        // 3 - The user wishes to remove this list from their favorites list. 
        console.log("In processFavModalSubmit")
        evt.preventDefault()

        if ((delFav).is(":checked")) { 
          delFavorites()
        } else { 
          saveOrEditFavorite(evt)
        } 
      }

      async function saveOrEditFavorite(evt) {

        // Retrieve key data from HTLM 
        const videoId = $("iframe").data('videoid')

        let fav_id = $("#favorites").data('fav_id')
        if (!fav_id) {
          fav_id = ""
        }

        // Collect data on the Add-Fav-Modal form 
        const inputVideoTitle = $("#input-video-title").val()
        const inputArtistName = $("#input-artist-name").val()
        const inputSongTitle =  $("#input-song-title").val()
        const inputVideoNotes =  $("#input-video-notes").val()


        params = {favId: fav_id,  id: videoId, title: inputVideoTitle, artist: inputArtistName,  song: inputSongTitle, notes: inputVideoNotes}

        try {
          // Send fav data to the server   
          const res = await axios.post('/favorites', params)    
          if (res.data) {  // Server was able to save data 

            // Save the DB id of the newly created favorite in the html
            $("#favorites").data('fav_id', res.data.fav_id) 

            // Update all fields on the Add Modal Form to reflect actual data saved in DB. Note: this is prob not needed. 
            $('#video-detail-title').text(res.data.video_title)
            $("#video-detail-artist").text(res.data.artist_name)
            $("#video-detail-song").text(res.data.song_title)
            $("#video-detail-notes").text(res.data.video_notes)

            // If the video wasn't a favorite before then change icon to show it is a favorite 
            if ($('#favorites i').hasClass('far fa-heart')) {
              // Toggle the favorites icon from the heart outlie to a solid red heart to indicate it's a favorite.
              $('#favorites i').toggleClass('far fa-heart fas fa-heart')
              // Show the notes sections
              $("#video-detail-notes-section").toggleClass('hide')
              $("#video-detail-notes").toggleClass('hide')
            }

            // Now that current video is a favorite show the notes field. 
            // $("#video-detail-notes-section").toggleClass('hide')
            // $("#video-detail-notes").toggleClass('hide')
            favSaveModal.modal('hide')
          }
        } catch(err) {
          console.log("Error message")
        }
      }

      vidDetailDelFav.addEventListener('click', delFavorites)      

      async function delFavorites(evt) {
        // If user clicks on the delete button in "Remove Fav" modal it will send a delete request to the server 

        // const favDelModal = $("#fav-delete-modal")
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
            // Hide the notes section
            $("#video-detail-notes-section").toggleClass('hide')
            $("#video-detail-notes").toggleClass('hide')
            // Hide the Delete warning message
            $('#del-fav-warning').toggleClass('hide')

            // Make sure delete checkbox is unchecked after a delete
            delFav. prop("checked", false);
            // Close the 
            favSaveModal.modal('hide')
            // favDelModal.modal('hide')
          }
        } catch(err) {
          console.log("Error message")
        }
      }
// }); 