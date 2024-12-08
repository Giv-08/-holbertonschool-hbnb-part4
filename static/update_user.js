// UPDATE USER
document.getElementById('update-form').addEventListener('submit', function(event) {
  event.preventDefault();  // Prevent form from submitting normally

  const userId = document.getElementById('user_id').value;
  const first_name = document.getElementById('first_name').value;
  const last_name = document.getElementById('last_name').value;
  const email = document.getElementById('email').value;

  const userData = {
      id: userId,
      first_name: first_name,
      last_name: last_name,
      email: email
  };

  console.log(userData);
  axios.put(`/update_user/${userId}`, userData)
      .then(response => {
          // Handle success
          alert('User updated successfully!');
          window.location.href = '/dashboard';
      })
      .catch(error => {
        if (error.response && error.response.data) {
          alert(error.response.data.message);
        } else {
            alert('Failed to update user details.');
        }
          console.error(error);
      });
});
