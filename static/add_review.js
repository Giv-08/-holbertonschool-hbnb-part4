const button = document.getElementById('submit-btn');
const text = document.querySelector('textarea');
const rating = document.getElementById('rating');

button.addEventListener('click', function() {
const reviewText = text.value;
const ratingText = parseInt(rating.value, 10); // must cast the type
const userId = document.getElementById('user_id').value;
const placeId = document.getElementById('place_id').value;

// Log the review data
// console.log({
//   text: reviewText,
//   rating: ratingText,
//   user_id: userId,
//   place_id: placeId
// }, {
//   headers: {
//     'Content-Type': 'application/json'
//   }
// });

// Send the data directly without wrapping it inside 'data'
axios.post('/api/v1/reviews/', {
  text: reviewText,
  rating: ratingText,
  user_id: userId,
  place_id: placeId
})
.then((response) => {
  // Redirect on success
  window.location.href = `/place/${placeId}`;
  console.log(response);
})
.catch((error) => {
  console.error('Error data:', error.response ? error.response.data : error.message);
});
})
