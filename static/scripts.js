// SEARCH FUNCTION
document.getElementById('search-btn').addEventListener('click', function() {
  const searchQuery = document.getElementById('search-box').value;
  const priceRange = document.getElementById('price-filter').value;
  let maxPrice = 0;
  switch(priceRange) {
      case "1":
          maxPrice = 250;
          break;
      case "2":
          maxPrice = 500;
          break;
      case "3":
          maxPrice = 1000;
          break;
      case "4":
          maxPrice = 3000;
          break;
      case "5":
          maxPrice = 7000;
          break;
      case "6":
          maxPrice = 10000;
          break;
      default:
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

          if (response.data && response.data.length > 0) {
            // Populate the new places based on the response
            response.data.forEach(function(place) {
                const placeItem = document.createElement('div'); // create a new div
                placeItem.classList.add('place-item'); // then add a class for div followed the existing index

                placeItem.innerHTML = `
                    <div class="image-box">
                        <img class="place-photo" src="https://media.gq.com/photos/66019f02c081abc36b271454/16:9/w_1280,c_limit/airbnb-art.jpg" alt="random_place_photo">
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
                            <p>Rating: ${(isNaN(place.average_rating)) ? 'Not rated' : (Math.round(place.average_rating * 100) / 100)}</p>
                        </div>
                    </div>
                    <div id="detail-btn-box">
                        <a id="detail-btn" href="/place/${place.place_id}">More details</a>
                    </div>
                `; // whole place card content
                placesList.appendChild(placeItem); // add at the end
              });
            } else {
              const text = document.createElement('span');
              const footer = document.querySelector('footer');
              const emoji = `<i class="fa-regular fa-face-frown"></i>`;

              text.innerHTML = `${emoji} No results found`;
              text.style.textAlign = 'center';
              text.style.position = 'absolute';
              text.style.fontSize = '2rem';
              placesList.appendChild(text);
              if (text.innerHTML === `${emoji} No results found`) {
                footer.style.bottom = '0';
              }
            }
          })
      .catch(function(error) {
          console.error("There was an error fetching the places:", error);
      });
});

// Add event listener for the 'Enter' key press in the search box
document.getElementById('search-box').addEventListener('keypress', function(event) { // grab the input
  if (event.key === 'Enter') {
    document.getElementById('search-btn').click();  // Trigger the search button click event
  }
});

// RESET BUTTON
document.getElementById('reset-btn').addEventListener('click', function() {
  document.getElementById('search-box').value = '';
  document.getElementById('price-filter').value = "6";

  const resetData = {
    name: '',
    price: 10000
  };

  axios.post('/api/v1/places/search', resetData)
    .then(function(response) { // fetch data once click function is triggered
        const placesList = document.querySelector('.places-container');
        placesList.innerHTML = '';
        // Populate the new places based on the response
        response.data.forEach(function(place) {
            const placeItem = document.createElement('div');
            placeItem.classList.add('place-item');

            placeItem.innerHTML = `
                <div class="image-box">
                    <img class="place-photo" src="https://media.gq.com/photos/66019f02c081abc36b271454/16:9/w_1280,c_limit/airbnb-art.jp" alt="random_place_photo">
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
                        <p>Rating: ${Math.round(place.average_rating * 100) / 100}</p>
                        </p>
                          </p>
                          </p>
                    </div>
                </div>
                <div id="detail-btn-box">
                    <a id="detail-btn" href="/place/${place.place_id}">More details</a>
                </div>
            `;
            placesList.appendChild(placeItem);
        });
    })
    .catch(function(error) {
        console.error("There was an error fetching the places:", error);
    });
});
