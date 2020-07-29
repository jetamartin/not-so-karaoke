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

/**************************************************************************************** 
 * Function:  processFavCardClickEvent
 * Only launch the favModal if the favIcon was clicked..otherwise just ignore the click
 * 
 * */ 
function processFavCardClickEvent(evt) {
  // Only lauch the Fav Modal if user has clicked on the Fav heart icon..otherwise ignore the click
  if (evt.target.className == 'fas fa-heart') {
    launchFavoritesModal(evt)
  }
}
  
/***********************************************************************************
 * Function:  launchFavoritesModal
* ---------------------------------------------------------------------------------------------
 * Called when the user clicks the Fav icon. This function. Performs the following:
 * 1) Fills in the modal form fields with data on the video card 
 * 2) Add the fav-id as a data element on modal save button to 'link' the modal 
 * back to a specific video card
 */
 function launchFavoritesModal (evt) {
  // Get the Favid of the video card that was clicked
  const fav_id = $(evt.target).closest('.favorites').data('fav_id')

  // Make sure the delete option is unchecked & the warning message is hidden when 
  // the user opens the Favorite model. This is needed to address scenrio where user 
  // clicks the deletes checkbox, cancels the modal and then re-opens modal window 
  // option
  if ((delFav).is(":checked")) { 
    // uncheck the checkbox and toggle the warning message
    delFav.prop('checked', false);
    delFavWarning.toggleClass('hide') 
  }

  // Get the values from the video detail card to populate the Fav modal form.
  const title = $(evt.target).closest('.fav-video-card').find('.video-detail-title').text()
  const artist = $(evt.target).closest('.fav-video-card').find('.video-detail-artist').text()
  const song = $(evt.target).closest('.fav-video-card').find('.video-detail-song').text()
  const notes = $(evt.target).closest('.fav-video-card').find('.video-detail-notes').text()

  
  // Now populate the Add-to-Favorites modal with the data from the video detail card
  inputVideoTitle.val(title)
  inputArtistName.val(artist)
  inputSongTitle.val(song)
  inputVideoNotes.val(notes) 

  // Saves a reference to video card (fav-id) as data attribute in the "Save" button 
  // so that the modal can be linked back to the video card and any action needed can
  // be peformed on the appropriate video card.  
  favModalSubmitBtn.data('fav_id', fav_id) 

  // Display the populated Add Favorite modal screen
  favModal.modal()
}

/***********************************************************************************************
 * Function:  processFavModalSubmit
* ---------------------------------------------------------------------------------------------
 * Called when the user clicks the "Save" button on the Fav Modal. It performs the following:
 * Determines if the user wants to remove (delete) the video card from the favorites list -OR-
 * wants to simply edit the favorite information and then calls the appropriate function to process
 * the "save" operation
*/
async function processFavModalSubmit(evt) {
  console.log("In processFavModalSubmit")
  evt.preventDefault()

  if ((delFav).is(":checked")) { 
    delFavorites(evt)
  } else { 
    editFavorite(evt)
  } 
}

/***********************************************************************************************
 * Function:  editFavorite
 * ---------------------------------------------------------------------------------------------
 * Called when user clicks save button (but has not selected 'delete" checkbox) on modal form. 
 * - Retrieves all fields from modal form  
 * - Sends this data (AJAX) to the server to update the Fav data DB for this video
 * - Handles response from server (including updating fields on modal form to show what was saved)
 * - And close the modal form
 * - TBD - Need to add more robust error handling for any failures that might occur
 *
*/
async function editFavorite(evt) {
  // Retrieve key data from HTLM 
  
  const fav_id = favModalSubmitBtn.data('fav_id')
  const card =  $('#'+fav_id)
  const title = card.find(".video-detail-title")
  const artist = card.find(".video-detail-artist")
  const song = card.find(".video-detail-song")
  const notes = card.find(".video-detail-notes")

  const video_thumbnail = card.find("img").attr('src')
  const videoId = card.find(".video-details").data('videoid')


  // Collect data on the Add-Fav-Modal form 
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

      // Update the modal form to reflect what is now stored in Db
      title.text(res.data.video_title) 
      artist.text(res.data.artist_name) 
      song.text(res.data.song_title)
      notes.text(res.data.video_notes)

      favModal.modal('hide')
    }
  } catch(err) { // AJAX call failed 
    console.log("Error message")
    // TBD - Design more robust error handling on client
    // 
  }
}

/***********************************************************************************************
 * Function:  delFavorite
 * ---------------------------------------------------------------------------------------------
 * Called when user clicks checks the 'delete" checkbox) on modal form and clicks modal save button
 * - Gets the fav-id for the video card from the modals save button via 'data' element 
 * - Sends AJAX delete request to server to remove the favorite from the Databse
 * - If the delete request was successful remove that video card from the client UI 
 * - And close the modal form
 * - TBD - Need to add more robust error handling for any failures that might occur
 *
*/
async function delFavorites(evt) {
  // If user clicks on the delete button in "Remove Fav" modal it will send a delete request to the server 

  // const favDelModal = $("#fav-delete-modal")
  console.log("Function delFavorites")

  const fav_id = favModalSubmitBtn.data('fav_id')
  const card =  $('#'+fav_id)

  try {
    const res = await axios.delete(`/favorites/${fav_id}`) 
    if (res.data) {
      console.log("Favorite was deleted")
      // Now remove the fav video card
      card.remove()

      // Close the 
      favModal.modal('hide')
      // favDelModal.modal('hide')
    }
  } catch(err) {
    console.log("Error message")
  }
}

/***************************************************************************************
 * Event listeners
 * 
 */
allVidCards.on('click', processFavCardClickEvent)
vidDetailFavSubmit.on('click', processFavModalSubmit)
delFav.on( "click", function() {
  delFavWarning.toggleClass('hide')
});
}); 