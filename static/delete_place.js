// DELETE PLACE
document.getElementById('delete-btn').addEventListener('click', function (e) {
  e.preventDefault(); // Prevent default behavior (if it's inside a form or link)
  const placeId = this.getAttribute('data-place-id'); // Get the place id from the button data attribute

  if (confirm('Are you sure you want to delete this item?')) {
    deletePlace(placeId);
  }

  function deletePlace(placeId) {
    axios.delete(`/update_place/${placeId}`)
      .then(function (response) {
        console.log('Place deleted successfully:', response);
        window.location.href = '/dashboard'; // Redirect to the dashboard after deletion
      })
      .catch(function (error) {
        console.error('Error deleting the place:', error);
        alert('Failed to delete the place. Please try again.');
      });
    }
});
