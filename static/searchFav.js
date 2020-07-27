$(document).ready(function () {

  const allVidCards = $("#vid-cards")
  const favModal = $('#fav-save-modal')
  const favModalSubmitBtn = $('#video-detail-fav-submit')
  const vidDetailFavSubmit = $("#video-detail-fav-submit")
  const delFav = $('#del-fav')
  const delFavWarning = $('#del-fav-warning')

  // Get handle for input fields on the favorite modal
  const inputVideoTitle = $('#input-video-title')
  const inputArtistName = $('#input-artist-name')
  const inputSongTitle = $('#input-song-title')
  const inputVideoNotes = $('#input-video-notes')


  function processFavCardClickEvent(evt) {
    // Only lauch the Fav Modal if user has clicked on the Fav heart icon..otherwise ignore the click
    console.log("In processFavCardClick function")
    if (evt.target.className == 'fas fa-heart' || evt.target.className == 'far fa-heart') {
      launchFavoritesModal(evt)
    }
  }
     
  function launchFavoritesModal (evt) {
   // Called when the user clicks the Fav icon
   // Fills in form fields based on which Fav video card was clicked
    const fav_id = $(evt.target).closest('.favorites').data('fav_id')
    const video_id = $(evt.target).closest('.card').data('videoid')
    
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
  
    // Display the populated Add Favorite modal screen
    favModal.modal()
  }
  
  
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
  
  async function editFavorite(evt) {
    // Allows user to make video a favorite or edit info in an existing favorite (e.g., add/change notes)
  
    // Retrieve key data from HTLM 
    const fav_id = favModalSubmitBtn.data('fav_id')
    const videoId = favModalSubmitBtn.data('videoid')
    const card =  $('#'+ videoId)
    const title = card.find(".video-detail-title")
    const artist = card.find(".video-detail-artist")
    const song = card.find(".video-detail-song")
    const notes = card.find(".video-detail-notes")
  
    const video_thumbnail = card.find("img").attr('src')
    // const videoId = card.find(".video-details").data('videoid')

    const inputVideoTitleVal = inputVideoTitle.val()
    const inputArtistNameVal = inputArtistName.val()
    const inputSongTitleVal =  inputSongTitle.val()
    const inputVideoNotesVal = inputVideoNotes.val()
  
  
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

          // Toggle the favorites icon from the heart outlie to a solid red heart to indicate it's a favorite.
          favIcon.toggleClass('far fa-heart fas fa-heart')

          // Show the notes sections
          card.find('.video-detail-notes-section').toggleClass('hide')
          // $("#video-detail-notes").toggleClass('hide')
  
        }
        favModal.modal('hide')
      }
    
    } catch(err) {
      console.log("Error message")
    }
  }
  
    
  async function delFavorites(evt) {
    // If user clicks on the delete button in "Remove Fav" modal it will send a delete request to the server 
  
    // const favDelModal = $("#fav-delete-modal")
    console.log("Function delFavorites")

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
  
        // Close the 
        favModal.modal('hide')
        // favDelModal.modal('hide')
      }
    } catch(err) {
      console.log("Error message")
    }
  }

  // ****************** Event listeners ************************* 
  vidDetailFavSubmit.on('click', processFavModalSubmit)
  allVidCards.on('click', processFavCardClickEvent )
  delFav.on( "click", function() {
    $('#del-fav-warning').toggleClass('hide')
  });

}); 