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

// axios.get('http://0.0.0.0:5000/api/v1/places/', {
//   headers: {
//     'Content-Type': 'application/json'
//   }
// })
// .then(response => {
//   console.log('Fetched data axios:', response.data);
//   const places = response.data;
// })
// .catch(error => {
//   console.error('Error fetching data:', error);
// });

// SEARCH FUNCTION
document.getElementById('search-btn').addEventListener('click', function() {
  const searchQuery = document.getElementById('seach-box').value;
  const priceRange = document.getElementById('price-filter').value;

  // Convert the selected price range to actual min and max values
  let minPrice = 0;
  let maxPrice = 0;
  switch(priceRange) {
      case "1":
          minPrice = 0;
          maxPrice = 250;
          break;
      case "2":
          minPrice = 250;
          maxPrice = 500;
          break;
      case "3":
          minPrice = 500;
          maxPrice = 1000;
          break;
      case "4":
          minPrice = 1000;
          maxPrice = 3000;
          break;
      case "5":
          minPrice = 3000;
          maxPrice = 7000;
          break;
      case "6":
          minPrice = 7000;
          maxPrice = 10000;
          break;
      default:
          minPrice = 0;
          maxPrice = 10000;
  }

  // Prepare the data to send in the POST request
  const data = {
      name: searchQuery, // the search input
      price: maxPrice  // Send max price for filtering
  };

  // Make the POST request to the search API endpoint
  axios.post('/api/v1/places/search', data)
      .then(function(response) { // fetch data once click function is triggered
          // Empty the div first
          const placesList = document.querySelector('.places-container');
          placesList.innerHTML = '';

          // Populate the new places based on the response
          response.data.forEach(function(place) {
              const placeItem = document.createElement('div'); // create a new div
              placeItem.classList.add('place-item'); // then add a class for div followed the existing index

              placeItem.innerHTML = `
                  <div class="image-box">
                      <img class="place-photo" src="https://media.istockphoto.com/id/1516933385/photo/3d-rendering-of-wooden-forest-house-surrounded-by-trees.jpg?s=612x612&w=0&k=20&c=gNMrzJw158wZaOg_vXgQ6obR0u2Vf4KghWLHxYD7_E8=" alt="random_place_photo">
                  </div>
                  <h2><i class="fa-solid fa-house-chimney"></i> ${place.title}</h2>
                  <p><i class="fa-solid fa-quote-left quote"></i>${place.description}<i class="fa-solid fa-quote-right quote"></i></p>
                  <div class="place-detail-box">
                      <div class="des-box">
                          <p><i class="fa-solid fa-location-dot"></i><strong>Latitude:</strong> ${place.latitude}</p>
                          <p><i class="fa-solid fa-location-dot"></i><strong>Longitude:</strong> ${place.longitude}</p>
                          <p><i class="fa-solid fa-dollar-sign"></i><strong>Price:</strong> ${place.price}</p>
                      </div>
                      <div class="rating-box">
                          <p>Rating: ${place.average_rating}</p>
                      </div>
                  </div>
                  <div id="detail-btn-box">
                      <a id="detail-btn" href="/place/${place.place_id}">More details</a>
                  </div>
              `; // whole place card content
              placesList.appendChild(placeItem); // add at the end
          });
      })
      .catch(function(error) { // if error
          console.error("There was an error fetching the places:", error);
      });
});

// Add event listener for the 'Enter' key press in the search box
document.getElementById('seach-box').addEventListener('keypress', function(event) { // grab the input
  if (event.key === 'Enter') {
    document.getElementById('search-btn').click();  // Trigger the search button click event
  }
});
