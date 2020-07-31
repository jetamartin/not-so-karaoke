/***********************************************************************************************
 * Function:  displayClientMsg(msg, status) - displays client pop up message on client
 * ---------------------------------------------------------------------------------------------
 * Called anytime a message needs to be displayed to client
 * - 
 *
*/
function displayClientMsg(msg, status, clientMsgs) {
  const show = 'show '
  // Add message to be displayed
  clientMsgs.text(msg)

  // Add the "show" class to DIV
  clientMsgs.addClass( show + status );

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ 
    clientMsgs.removeClass()
    clientMsgs.text("") 
  }, 3000);
}
