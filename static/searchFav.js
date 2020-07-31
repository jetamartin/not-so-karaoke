$(document).ready(function () {

  // Client side messages for Favorite updates
  const FAV_ADDED = "Added Favorite"
  const FAV_UPDATED = "Updated Favorite"
  const FAV_DELETED = "Deleted Favorite"
  const FAV_ADD_UPDATE_FAILED = "Favorite Add/Update Failed"
  const FAV_DELETE_FAILED = "Favorite Deletion Failed"

  // Key constants/references (e.g., html fields for modal form)
  const allVidCards = $("#vid-cards")
  const favModal = $('#fav-save-modal')
  const favModalSubmitBtn = $('#video-detail-fav-submit')
  const vidDetailFavSubmit = $("#video-detail-fav-submit")
  const delFav = $('#del-fav')
  const delFavWarning = $('#del-fav-warning')
  const favDelCheckbox = $('#fav-del-checkbox')

  // Get handle for input fields on the favorite modal
  const inputVideoTitle = $('#input-video-title')
  const inputArtistName = $('#input-artist-name')
  const inputSongTitle = $('#input-song-title')
  const inputVideoNotes = $('#input-video-notes')

  const clientMsgs = $('#client-msgs')


/***********************************************************************************************
 * Function:  processFavCardClicked
 * ---------------------------------------------------------------------------------------------
 * Called anytime a user clicks in the search video results area
 * - If the user clicked on the fav icon in any of the cards it launches the function to launch
 *   the fav modal otherwise the click is ignored
 *
*/
  function processFavCardClickEvent(evt) {
    // Only lauch the Fav Modal if user has clicked on the Fav heart icon..otherwise ignore the click
    console.log("In processFavCardClick function")
    if (evt.target.className == 'fas fa-heart' || evt.target.className == 'far fa-heart') {
      launchFavoritesModal(evt)
    }
  }

  /***********************************************************************************************
 * Function:  lauchFavoritesModal
 * ---------------------------------------------------------------------------------------------
 * Called anytime a user clicks on the fav icon on a video card in the search results
 * - Reinitialize the Delete warning (hide it) if it was clicked on the prior save
 * - Populate the modal form fields from the video card that was clicked
 * - Save the fav-id and the video_id as a data element on the modal Save button so that the 
 *   modal window can be linked back to the select video card
 * - Finally display the filled in modal window
*/
  function launchFavoritesModal (evt) {
   // Called when the user clicks the Fav icon
   // Fills in form fields based on which Fav video card was clicked
    const fav_id = $(evt.target).closest('.favorites').data('fav_id')
    const video_id = $(evt.target).closest('.card').data('videoid')
    const userId = $(evt.target).closest('.card').data('user_id')

    // Only show Fav modal if a user is logged in otherwise the modal will be disabled.
    // if the fav modal is enabled it seems to automatically disable the tooltip which is the desired behavior 
    if (userId) {
    
      // Make sure the delete option is unchecked & the warning message is hidden when 
      // the user opens the Favorite model. This is needed to address scenrio  where user 
      // clicks the deletes checkbox, cancels the modal and then re-opens modal window 
      // option
      if ((delFav).is(":checked")) { 
        // uncheck the checkbox and hide the warning message
        delFav.prop('checked', false);
        delFavWarning.toggleClass('hide') 
      }
    
      // Get the values from the video detail card to populate the 'Add to favorites' modal form.
      const title = $(evt.target).closest('.video-card').find('.video-detail-title').text()
      const artist = $(evt.target).closest('.video-card').find('.video-detail-artist').text()
      const song = $(evt.target).closest('.video-card').find('.video-detail-song').text()
      const notes = $(evt.target).closest('.video-card').find('.video-detail-notes').text()
    
      // Now populate the Add-to-Favorites modal with the data from the video detail card
      inputVideoTitle.val(title)
      inputArtistName.val(artist)
      inputSongTitle.val(song)
      inputVideoNotes.val(notes) 
    
      // Saves a reference to video card (fav-id) as data attribute in the "Save" button 
      // so that the modal can be linked back to the video card and any action needed will
      // be peformed on that video card.  
      favModalSubmitBtn.data('fav_id', fav_id) 
      favModalSubmitBtn.data('videoid', video_id)

      // Scenario 1:  Current video is not a favorite
      if ( event.target.className == 'far fa-heart' ) { 
        inputVideoNotes.val("") 
        // Hide the delete check box because this video isn't a favorite yet 
        favDelCheckbox.addClass('hide')
      
      } else {  // Current video is already a fav and user wants to remove it as a favorite video

        // Display the Delete checkbox by removing 'hide' class
        favDelCheckbox.removeClass('hide')
      }

      // Display the populated Add Favorite modal screen
      favModal.modal()
    } else { // User is not logged in 
      // // Show tooltip if non-login user hovers over favorite icon.
      // $('[data-toggle="tooltip"]').tooltip({
      //   title : "Login/Signup to mark video as a Favorite.",
      //   placement : 'top'
      // });
    }
  }
  
 /***********************************************************************************************
 * Function:  processFavModalSubmit()
 * ---------------------------------------------------------------------------------------------
 * Called when the user clicks "Save" button on the modal form
 * - Checks to see if the user clicked the "delete" checkbox and if so calls function to delete fav
 * - Otherwise it calls the function to save the user fav edits
*/
  async function processFavModalSubmit(evt) {
  // Called when the user clicks the "Save" button on the Fav Modal
  // Determines if the delete checkbox is checked and takes approriate action
    console.log("In processFavModalSubmit")
    evt.preventDefault()

    // If the delete checkbox on Fav modal has been checked then user wants to remove video as a favorite
      if ((delFav).is(":checked")) { 
      delFavorites(evt)
    } else {  // User wants to add this video to favorite or edit this favorite (e.g., add user notes)
      editFavorite(evt)
    } 
  }


 /***********************************************************************************************
 * Function:  editFavorite() - Send ajax request to server to create/edit a favorite
 * ---------------------------------------------------------------------------------------------
 * Called when the user clicks "Save" button on the modal form without checking the delete checkbox
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
   async function editFavorite(evt) {
    // Allows user to make video a favorite or edit info in an existing favorite (e.g., add/change notes)
  
    // Get key data from modal save button to connect this save to video card
    const fav_id = favModalSubmitBtn.data('fav_id')
    const videoId = favModalSubmitBtn.data('videoid')
    const card =  $('#'+ videoId)

    // Now retrieve references to key fields of the video card
    const title = card.find(".video-detail-title")
    const artist = card.find(".video-detail-artist")
    const song = card.find(".video-detail-song")
    const notes = card.find(".video-detail-notes")
    const video_thumbnail = card.find("img").attr('src')

    // Get the values present on the fav modal form
    const inputVideoTitleVal = inputVideoTitle.val()
    const inputArtistNameVal = inputArtistName.val()
    const inputSongTitleVal =  inputSongTitle.val()
    const inputVideoNotesVal = inputVideoNotes.val()
  
    // Include key values to update the fav table in DB
    params = {favId: fav_id,
              id: videoId, 
              thumbnail: video_thumbnail,
              title: inputVideoTitleVal,
              artist: inputArtistNameVal,  
              song: inputSongTitleVal, 
              notes: inputVideoNotesVal, }
  
    try {
      // Send fav data to the server so this fav can be added or updated  
      const res = await axios.post('/favorites', params)    
      if (res.data) {  // Server was able to save data 
  
        // Update the video card to reflect data that was saved on modal form
        title.text(res.data.video_title) 
        artist.text(res.data.artist_name) 
        song.text(res.data.song_title)
        notes.text(res.data.video_notes)
        favIcon = $('#'+videoId).find('.favorites i')
        
        // If the video wasn't a favorite before then change icon to show it is a favorite 
        if (favIcon.hasClass("far fa-heart")) {

          // Save the DB id of the newly created favorite in the html
          card.find('.favorites').data('fav_id', res.data.fav_id)

          // Toggle the favorites icon from the heart outline to a solid red heart to indicate it's a favorite.
          favIcon.toggleClass('far fa-heart fas fa-heart')

          // Show the notes sections
          card.find('.video-detail-notes-section').toggleClass('hide')

          // Display message to client
          displayClientMsg(FAV_ADDED, 'success', clientMsgs)


        } else {  // User is updating an existing favorite
        
          // Display message to client
          displayClientMsg(FAV_UPDATED, 'success', clientMsgs)

        }
        favModal.modal('hide')
      }
    
    } catch(err) {
        displayClientMsg(FAV_ADD_UPDATE_FAILED, 'error', clientMsgs)
        favModal.modal('hide')
        console.log("Error message")
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
  
    const fav_id = favModalSubmitBtn.data('fav_id')
    videoId = $(evt.target).data('videoid')
    const card =  $('#'+videoId)
  
    try {
      const res = await axios.delete(`/favorites/${fav_id}`) 
      if (res.data) {


        console.log("Favorite was deleted")
        favIcon = $('#'+videoId).find('.favorites i')       
        favIcon.toggleClass('far fa-heart fas fa-heart')

        // Now that card is no longer a favorite remove it's fav_id from card
        card.find('.favorites').data('fav_id', '')

        // Remove fav_id from modal submit button so that modal is 
        // no longer connected to now deleted card
        favModalSubmitBtn.data('fav_id', "")

        // Clear out notes value from Card
        card.find('.video-detail-notes').text("")
        // Hide the notes section
        card.find('.video-detail-notes-section').toggleClass('hide')

         // Hide the Delete warning message
        $('#del-fav-warning').toggleClass('hide')

        // Clear out all fields on modal form
        inputVideoTitle.val("") 
        inputArtistName.val("")
        inputSongTitle.val("")
        inputVideoNotes.val("")
        // Make sure delete checkbox is unchecked after a delete
        delFav. prop("checked", false);

        displayClientMsg(FAV_DELETED, 'success', clientMsgs)

        // Close the 
        favModal.modal('hide')
      }
    } catch(err) {
      console.log("Error message")
      favModal.modal('hide')
      displayClientMsg(FAV_DELETE_FAILED, 'error', clientMsgs)

      // TBD improve error handline
    }
  }

  /****************************************************************************************
   * Event listeners
   * ---------------------------------------------------------------------------------------
   */
  vidDetailFavSubmit.on('click', processFavModalSubmit)
  allVidCards.on('click', processFavCardClickEvent )
  delFav.on( "click", function() {
    $('#del-fav-warning').toggleClass('hide')
  });
  // Show tooltip if non-login user hovers over favorite icon.
  $('[data-toggle="tooltip"]').tooltip({
    title : "Login/Signup to mark video as a Favorite.",
    placement : 'top'
  });

}); 



