// UPDATE PLACE
    document.getElementById('update-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent form from submitting normally

        const placeId = document.getElementById('place_id').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const price = parseFloat(document.getElementById('price').value);

        if (isNaN(price)) {
          alert("Invalid price");
          return;
        }

        const placeData = {
            id: placeId,
            title: title,
            description: description,
            price: parseFloat(price)
        };

        console.log(placeData);
        axios.put(`/update_place/${placeId}`, placeData)
            .then(response => {
                // Handle success
                alert('Place updated successfully!');
                window.location.href = '/dashboard';
            })
            .catch(error => {
                // Handle error
                alert('Failed to update place.');
                console.error(error);
            });
    });
