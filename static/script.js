document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Code to refresh photo grid after upload
    })
    .catch(error => console.error('Error:', error));
});

// Fetch photos from the back end and display them in the grid
function fetchPhotos() {
    fetch('/photos')
        .then(response => response.json())
        .then(data => {
            const photoGrid = document.getElementById('photoGrid');
            photoGrid.innerHTML = ''; // Clear existing photos

            data.forEach(photo => {
                const img = document.createElement('img');
                img.src = photo.path; // Adjust according to your photo structure
                photoGrid.appendChild(img);
            });
        });
}

fetchPhotos(); // Initial fetch on page load
