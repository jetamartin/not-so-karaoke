// $(document).ready(function () {

const allVidCards = document.getElementById("vid-cards")
const favModal = $('#fav-save-modal')
const favModalSubmitBtn = $('#video-detail-fav-submit')

const vidDetailFavSubmit = document.getElementById("video-detail-fav-submit")
const vidDetailDelFav = document.getElementById("video-detail-delete-fav")
// const favSaveModal = $("#fav-save-modal")
const delFav = $('#del-fav')
const delFavWarning = $('#del-fav-warning')

allVidCards.addEventListener('click', processFavCardClickEvent)

function processFavCardClickEvent(evt) {
  // Only lauch the Fav Modal if user has clicked on the Fav heart icon..otherwise ignore the click
  console.log("In processFavCardClick function")
  if (evt.target.className == 'fas fa-heart') {
    launchFavoritesModal(evt)
  }
}
   
function launchFavoritesModal (evt) {
 // Called when the user clicks the Fav icon
 // Fills in form fields based on which Fav video card was clicked
  const fav_id = $(evt.target).closest('.favorites').data('fav_id')


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
  const title = $(evt.target).closest('.fav-video-card').find('.video-detail-title').text()
  const artist = $(evt.target).closest('.fav-video-card').find('.video-detail-artist').text()
  const song = $(evt.target).closest('.fav-video-card').find('.video-detail-song').text()
  const notes = $(evt.target).closest('.fav-video-card').find('.video-detail-notes').text()

  // Get handle for input fields on the favorite modal
  inputVideoTitle = $('#input-video-title')
  inputArtistName = $('#input-artist-name')
  inputSongTitle = $('#input-song-title')
  inputVideoNotes = $('#input-video-notes')

  // Now populate the Add-to-Favorites modal with the data from the video detail card
  inputVideoTitle.val(title)
  inputArtistName.val(artist)
  inputSongTitle.val(song)
  inputVideoNotes.val(notes) 

  // Saves a reference to video card (fav-id) as data attribute in the "Save" button 
  // so that the modal can be linked back to the video card and any action needed wil
  // be peformed on that video card.  
  favModalSubmitBtn.data('fav_id', fav_id) 

  // Display the populated Add Favorite modal screen
  favModal.modal()
}


delFav.on( "click", function() {
  $('#del-fav-warning').toggleClass('hide')
});

vidDetailFavSubmit.addEventListener('click', processFavModalSubmit)

async function processFavModalSubmit(evt) {
// Called when the user clicks the "Save" button on the Fav Modal
// Determines if the delete checkbox is checked and takes approriate action
  console.log("In processFavModalSubmit")
  evt.preventDefault()

  if ((delFav).is(":checked")) { 
    delFavorites(evt)
  } else { 
    editFavorite(evt)
  } 
}

async function editFavorite(evt) {

  // Retrieve key data from HTLM 
  // "$('#'+fav_id)[0]"  This will find the video card that was originally clicked
  const fav_id = favModalSubmitBtn.data('fav_id')
  const card =  $('#'+fav_id)
  const title = card.find(".video-detail-title")
  const artist = card.find(".video-detail-artist")
  const song = card.find(".video-detail-song")
  const notes = card.find(".video-detail-notes")

  const video_thumbnail = card.find("img").attr('src')
  const videoId = card.find(".video-details").data('videoid')


  // Collect data on the Add-Fav-Modal form 
  const inputVideoTitle = $("#input-video-title").val()
  const inputArtistName = $("#input-artist-name").val()
  const inputSongTitle =  $("#input-song-title").val()
  const inputVideoNotes =  $("#input-video-notes").val()


  params = {favId: fav_id,
            id: videoId, 
            thumbnail: video_thumbnail,
            title: inputVideoTitle,
            artist: inputArtistName,  
            song: inputSongTitle, 
            notes: inputVideoNotes, }

  try {
    // Send fav data to the server   
    const res = await axios.post('/favorites', params)    
    if (res.data) {  // Server was able to save data 

      title.text(res.data.video_title) 
      artist.text(res.data.artist_name) 
      song.text(res.data.song_title)
      notes.text(res.data.video_notes)

      favModal.modal('hide')
    }
  } catch(err) {
    console.log("Error message")
  }
}

// vidDetailDelFav.addEventListener('click', delFavorites)      

async function delFavorites(evt) {
  // If user clicks on the delete button in "Remove Fav" modal it will send a delete request to the server 

  // const favDelModal = $("#fav-delete-modal")
  console.log("Function delFavorites")

  // // Get the videoId from the details page
  // videoId = $("#video-details").data('videoid')
  // userId = $("#video-details").data('user_id')
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
// }); 