console.log("I'm in viewVideo.js file")

const favorites = document.getElementById("favorites")
const vidDetailFavSubmit = document.getElementById("video-detail-fav-submit")
const vidDetailDelFav = document.getElementById("video-detail-delete-fav")
const favSaveModal = $("#fav-save-modal")
const delFav = $('#del-fav')

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
  const video_thumbnail = $('#video-details').data('thumbnail')

  let fav_id = $("#favorites").data('fav_id')
  if (!fav_id) {
    fav_id = ""
  }

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