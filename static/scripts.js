/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

// document.addEventListener('DOMContentLoaded', () => {
//   // When the DOM is loaded, fetch data from the API
//   axios.get('http://localhost:5000/api/v1/places/')
//     .then(response => {
//       console.log(response.data);  // You can access the data via response.data
//     })
//     .catch(error => {
//       console.error('Error fetching data:', error);
//     });
// });

// flask run --port=5001
axios.get('http://0.0.0.0:5000/api/v1/places/', {
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('Fetched data:', response.data);
  const places = response.data;
  console.log('Places:', places);
})
.catch(error => {
  console.error('Error fetching data:', error);
});
