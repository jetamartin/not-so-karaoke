// $(document).ready(function () {



const playerDiv = $('#player')

// Client side messages for Favorite updates
const FAV_ADDED = "Added Favorite"
const FAV_UPDATED = "Updated Favorite"
const FAV_DELETED = "Deleted Favorite"
const FAV_ADD_UPDATE_FAILED = "Favorite Add/Update Failed"
const FAV_DELETE_FAILED = "Favorite Deletion Failed"
const clientMsgs = $('#client-msgs')


const altLyricsSearchForm = $('#lyrics-search-form')
// const lyricsSearch = document.getElementById("lyrics-search-form")
const lyricsSearchResults = $("#lyrics-search-results")
const altLyricsContent = $("#lyrics-content")
const altLyricsInputArtistName = $("#artist")
const altLyricsInputSongTitle = $("#song")

const favorites = $('#favorites')
const favIcon = $('#favorites i')
const vidDetails = $("#video-details")

const vidDetailFavSubmit = $("#video-detail-fav-submit")
const vidDetailDelFav = $("#video-detail-delete-fav")
const favSaveModal = $("#fav-save-modal")
const delFav = $('#del-fav')
const delFavWarning = $('#del-fav-warning')
const favDelCheckbox = $('#fav-del-checkbox')


// Get the values from the video detail card to populate the 'Add to favorites' modal form.
const videoDetailTitle = $("#video-detail-title")
const videoDetailArtist = $("#video-detail-artist")
const videoDetailSong =  $("#video-detail-song")
const videoDetailNotes =  $("#video-detail-notes")
const videoDetailNotesSection = $("#video-detail-notes-section")

// Get handle for input fields on the favorite modal
const inputVideoTitle = $('#input-video-title')
const inputArtistName = $('#input-artist-name')
const inputSongTitle = $('#input-song-title')
const inputVideoNotes = $('#input-video-notes')



// $(document).ready(function () {


/***********************************************************************************************
 * Function:  displayClientMsg(msg, status) - displays client pop up message on client
 * ---------------------------------------------------------------------------------------------
 * Called anytime a message needs to be displayed to client
 * - 
 *
*/
    // function displayClientMsg(msg, status, clientMsgs) {
    //   const show = 'show '
    //   // Add message to be displayed
    //   clientMsgs.text(msg)

    //   // Add the "show" class to DIV
    //   clientMsgs.addClass( show + status );

    //   // After 3 seconds, remove the show class from DIV
    //   setTimeout(function(){ 
    //     clientMsgs.removeClass()
    //     clientMsgs.text("") 
    //   }, 3000);
    // }
      
    console.log("I'm in viewVideo.js file")


    //This code loads the IFrame Player API code asynchronously.
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // 3. This function creates an <iframe> (and YouTube player)
    //    after the API code downloads.
    var player;

    /***********************************************************************************************
     * Function:  onYouTubePlayerAPIReady() - set key params for YT Player
    * ---------------------------------------------------------------------------------------------
    * Set key parameters for YT Player
    * Create methods to handle various play states
    */
    function onYouTubePlayerAPIReady() {
      player = new YT.Player('player', {
        playerVars: { 'autoplay': 0, 'controls': 1, 'fs': 0},
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange,
          'onError': onError
        }
      });
    }

    /***********************************************************************************************
     * Function:  onYouTubePlayerAPIReady() - queues up video for play when video playe is ready
    * ---------------------------------------------------------------------------------------------
    * YT API will call this function when the video player is ready
    * Create methods to handle various play states
    */
    function onPlayerReady(event) {
  
      console.log("*****OnPlayerReady Function")

      // iFrame is generated dynamically via YT api
      const videoId = $("iframe").data('videoid')

      // Cues up the video...user must press play to play video
      player.cueVideoById(videoId)

      // Limits the amount of space the lyrics will consume to match height of video
      // ===> Note this func is not currently being used but is being kept for reference for future enhancements
      // lyricElementResize()
    }

    /***********************************************************************************************
    * Function:  onPlayerStateChange() - called when the player state changes
    * ---------------------------------------------------------------------------------------------
    * Not currently being used but here as a placeholder for when new functionality is added
    * 
    */
    function onPlayerStateChange(event) {

    }

    /***********************************************************************************************
    * Function:  onError() - called whenever an error is detected
    * ---------------------------------------------------------------------------------------------
    * Not currently being used but here as a placeholder for when new functionality is added
    * 
    */
    function onError(event) {
      console.log("in onError function", event)
      console.log('Error message: ', event)
    }

    /***********************************************************************************************
    * Function:  lyricElementResize() - restricts the height of lyrics to height of video
    * ---------------------------------------------------------------------------------------------
    * Not currently being used but here as a placeholder for when new functionality is added
    * 
    */
    function lyricElementResize() {
      console.log("lyricElementResize() - Triggered ")
      var videoFrame = document.getElementById("player");
      var videoHeight = videoFrame.offsetHeight;
      console.log("*********videoHeight", videoHeight);
      var lyricFrame = document.getElementById("lyrics")
      lyricFrame.style.maxHeight = videoHeight + "px";
    }

    /***********************************************************************************************
    * Function:  requestMoreLyrics() - allows user to request a different set of lyrics
    * ---------------------------------------------------------------------------------------------
    * Called when the user clicks the submit button on the lyrics input form from this view-video page
    * - Gets the user input (artist & song title) from the lyrics search form
    * - Sends lyrics request to Server via an AJAX
    * - If request was successful display new lyrics in UI else log and error
    */
    async function requestMoreLyrics(evt) {
      console.log("Process the submit Lyrics request form")
      evt.preventDefault()
      const inputArtistName = altLyricsInputArtistName.val()
      const inputSongTitle = altLyricsInputSongTitle.val()

      params = {artist: inputArtistName, song: inputSongTitle}

      try {
        const res = await axios.post('http://localHost:5000/lyrics', params)    
        if (res.data) {
          altLyricsContent.html(res.data) 
        }
      } catch(err) {
        console.log("Error message")
        // TBD - beef up error handling
      }
    }

  /***********************************************************************************************
   * Function:  lauchFavoritesModal
   * ---------------------------------------------------------------------------------------------
   * Called anytime a user clicks on the fav icon on a video card in the view video screen
   * - Reinitialize the Delete warning (hide it) if it was clicked on the prior save
   * - Populate the modal form fields from the video card that was clicked
   * - If the vide wasn't previously a fav then clear the notes and hide the delete checkbox
   * - Otherwise (already a favorite) show the delete checkbox
   * - Finally display the filled in modal window
  */
    function launchFavoritesModal (evt) {
      // Launches the Modal window
      
      userId = vidDetails.data('user_id')

      // Only show Fav modal if a user is logged in otherwise the modal will be disabled.
      // if the fav modal is enabled it seems to automatically disable the tooltip which is the desired behavior 
      if (userId) {
        // Make sure the delete option is unchecked & the warning message is hidden when 
        // the user opens the Favorite model. This is needed to address scenrio  where user 
        // clicks the deletes checkbox, cancels the modal and then re-opens modal window 
        // option
        if ((delFav).is(":checked")) { 
          // uncheck the checkbox and toggle the warning message
          delFav.prop('checked', false);
          delFavWarning.toggleClass('hide') 
        }

        // Get the values from the video detail card to populate the 'Add to favorites' modal form.
        videoDetailTitleContent = videoDetailTitle.text()
        videoDetailArtistContent = videoDetailArtist.text()
        videoDetailSongContent =  videoDetailSong.text()
        videoDetailNotesContent =  videoDetailNotes.text()

        // Now populate the Add-to-Favorites modal with the data from the video detail card
        inputVideoTitle.val(videoDetailTitleContent)
        inputArtistName.val(videoDetailArtistContent)
        inputSongTitle.val(videoDetailSongContent)
        inputVideoNotes.val(videoDetailNotesContent) 

        // Display the populated Add Favorite modal screen
        favSaveModal.modal()

        // Scenario 1:  Current video is not a favorite
        if ( event.target.className == 'far fa-heart' ) { 
          inputVideoNotes.val("") 
          // Hide the delete check box because this video isn't a favorite yet 
          favDelCheckbox.addClass('hide')
        
        } else {  // Current video is already a fav and user wants to remove it as a favorite video

          // Display the Delete checkbox by removing 'hide' class
          favDelCheckbox.removeClass('hide')
        }

      } else { // no user is logged in
        
        // Show tooltip if non-login user hovers over favorite icon.
        // $('[data-toggle="tooltip"]').tooltip({
        //   title : "Login/Signup to mark video as a Favorite.",
        //   placement : 'top'
        // });

      }
    }

    /***********************************************************************************************
     * Function:  processFavModalSubmit() - determines user wants to remove or save/update fav video
     * ---------------------------------------------------------------------------------------------
     * Called when the user clicks "Save" button on the modal form
     * - Checks to see if the user clicked the "delete" checkbox and if so calls function to delete fav
     * - Otherwise it calls the function to create/save the user fav edits
    */
    async function processFavModalSubmit(evt) {
      evt.preventDefault()

      if ((delFav).is(":checked")) { 
        delFavorites()
      } else { 
        saveOrEditFavorite(evt)
      } 
    }

  /***********************************************************************************************
   * Function:  saveOrEditFavorite() - Send ajax request to server to create/edit a favorite
   * ---------------------------------------------------------------------------------------------
   * Called when the user clicks "Save" button on the modal form but doesn't check the delete checkbox
   * 
   * - Retrieves fav data entered by user and/or from video card 
   * - Once the data is collected an Ajax call is made to the server to save the data in the Fav DB table
   * - If the fav is saved successfully then:
   * --- the video card is updated 
   * --- the fav-id is saved in the video cards html
   * --- if a new fav has been created then the fav icon is changed to a solid red heart
   * --- and the notes section is displayed
   * --- finally hide the modal
   * - TBD - Error handling if save fails for some reason
   */
    async function saveOrEditFavorite(evt) {

      // Retrieve key data from HTLM 
      const videoId = $("iframe").data('videoid')
      const video_thumbnail = vidDetails.data('thumbnail')

      // Get the fav-id (if present) from the video card otherwise set fav_id to ""
      let fav_id = favorites.data('fav_id')
      if (!fav_id) {
        fav_id = ""
      }

      // Collect data on the Add-Fav-Modal form 
      const inputVideoTitleVal = inputVideoTitle.val()
      const inputArtistNameVal = inputArtistName.val()
      const inputSongTitleVal =  inputSongTitle.val()
      const inputVideoNotesVal =  inputVideoNotes.val()

      params = {favId: fav_id,
                id: videoId, 
                thumbnail: video_thumbnail,
                title: inputVideoTitleVal,
                artist: inputArtistNameVal,  
                song: inputSongTitleVal, 
                notes: inputVideoNotesVal, }

      try {
        // Send fav data to the server   
        const res = await axios.post('/favorites', params)    
        if (res.data) {  // Server was able to save data 

          // Save the DB id of the newly created favorite in the html
          favorites.data('fav_id', res.data.fav_id) 

          // Update all fields on the Add Modal Form to reflect actual data saved in DB. Note: this is prob not needed. 
          videoDetailArtist.text(res.data.video_title)
          videoDetailArtist.text(res.data.artist_name)
          videoDetailSong.text(res.data.song_title)
          videoDetailNotes.text(res.data.video_notes)

          // If the video wasn't a favorite before then change icon to show it is a favorite 
          if (favIcon.hasClass('far fa-heart')) {
            // Toggle the favorites icon from the heart outlie to a solid red heart to indicate it's a favorite.
            favIcon.toggleClass('far fa-heart fas fa-heart')
            // Show the notes sections
            videoDetailNotesSection.toggleClass('hide')
            videoDetailNotes.toggleClass('hide')
            // Display message to client
            displayClientMsg(FAV_ADDED, 'success', clientMsgs)

          } else {  // video already marked as a favorite and the user is updating favorite
            displayClientMsg(FAV_UPDATED, 'success', clientMsgs)
          }

          favSaveModal.modal('hide')
        }
      } catch(err) {
        console.log("Error message")
        displayClientMsg(FAV_ADD_UPDATE_FAILED, 'error', clientMsgs)

      }
    }

  /***********************************************************************************************
   * Function:  delFavorites() - Send ajax request to remove the video from the favorites list
   * ---------------------------------------------------------------------------------------------
   * Called when the user clicks "Save" button on the modal form AND has checked the delete checkbox
   *
   * - For the video that was originally clicked send a request to the server to remove this 
   * video from the favorites list:
   * --- remove the fav-id from the card and remove the fav-id from the modal's save button data attribute
   * --- toggle the favIcon from a solid red heart icon  (favorite) to a heart outline
   * --- clear out the notes section and hide the notes 
   * --- clear out the modal form fields 
   * --- make sure that the delete checkbox is reset
   * --- finally hide the modal
   * - TBD - Error handling if save fails for some reason
   */
    async function delFavorites(evt) {
      // If user clicks on the delete button in "Remove Fav" modal it will send a delete request to the server 

      // const favDelModal = $("#fav-delete-modal")
      console.log("Function delFavorites")

      // Get the videoId from the details page
      videoId = $("iframe").data('videoid')
      userId = $("iframe").data('user_id')
      fav_id = favorites.data('fav_id')

      try {
        const res = await axios.delete(`/favorites/${fav_id}`) 
        if (res.data) {
          console.log("Favorite was deleted")
          favIcon.toggleClass('far fa-heart fas fa-heart')
          favorites.data("fav_id", "")
          // Hide the notes section
          videoDetailNotesSection.toggleClass('hide')
          videoDetailNotes.toggleClass('hide')
          // Hide the Delete warning message
          delFavWarning.toggleClass('hide')

          // Make sure delete checkbox is unchecked after a delete
          delFav. prop("checked", false);

          displayClientMsg(FAV_DELETED, 'success', clientMsgs)

          // Close the modal
          favSaveModal.modal('hide')
          // favDelModal.modal('hide')
        }
      } catch(err) {
        displayClientMsg(FAV_DELETE_FAILED, 'error', clientMsgs)
        // Close the modal
        favSaveModal.modal('hide')
        console.log("Error message")
      }
    }

  /***************************************************************************************
   * 
   * Event listeners
   * 
   ***************************************************************************************/
    delFav.on( "click", function() {
      delFavWarning.toggleClass('hide')
      });
  
      vidDetailFavSubmit.on('click', processFavModalSubmit)

      altLyricsSearchForm.on('submit', requestMoreLyrics)
    
      favorites.on('click', launchFavoritesModal)
  
      // Show tooltip if non-login user hovers over favorite icon.
      $('[data-toggle="tooltip"]').tooltip({
        title : "Login/Signup to mark video as a Favorite.",
        placement : 'top'
      });
// }); 