// DISPLAY LOGGED IN MESSAGE FOR 5 SECS
setTimeout(function loginMessage() {
  let login = document.getElementById('flash-message-login');
  let logout = document.getElementById('flash-message-logout');
  if (login) {
    login.style.display = 'none';
  }
}, 1000); // after 3 secs, it disappears

// DISPLAY LOGGED OUT MESSAGE FOR 5 SECS
// setTimeout(function logoutMessage() {
//   document.getElementById('flash-message-logout').style.display = 'none';
// }, 3000); // after 3 secs, it disappears
