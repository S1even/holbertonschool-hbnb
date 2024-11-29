document.addEventListener('DOMContentLoaded', function () {
    // nav-loader
    fetch('static/element.html')
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            document.querySelector('nav').innerHTML = doc.querySelector('nav').innerHTML;
            document.querySelector('footer').innerHTML = doc.querySelector('footer').innerHTML;

            // Check user authentication after loading the nav and footer
            checkAuthentication();
        })
        .catch(error => console.error('Nav or Footer loading error:', error));

        
    // login-loader
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=3600; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Login failed:', error);
                alert('An error occurred while logging in');
            }
        });
    }


    // Change rating note in stars
    const ratingLinks = document.querySelectorAll('.rating a');
    ratingLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const ratingValue = this.getAttribute('href').substring(1);
            console.log(`${ratingValue} stars!`);
        });
    });


    // Populate the price filter dropdown
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.innerHTML = `
            <option value="All">All</option>
            <option value="10">$10</option>
            <option value="50">$50</option>
            <option value="100">$100</option>
        `;

        // Implement client-side filtering
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');
            placeCards.forEach(card => {
                const priceText = card.querySelector('p').textContent;
                const price = parseInt(priceText.replace('Price per night: $', ''));
                if (selectedPrice === 'All' || price <= parseInt(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }


    // Event listener for review form submission
    const reviewForm = document.getElementById('review-form');
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            await submitReview(token, placeId, reviewText);
        });
    }
});


// Function to check user authentication based on token
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }
}


// Function to get a specific cookie value by name
function getCookie(cookie_name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${cookie_name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


// Fetch places data dynamically if the user is authenticated
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });
        if (response.ok) {
            const places = await response.json();
            console.log('Places data:', places);
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}


// Function to populate the places list dynamically
function displayPlaces(places) {
    const placesListSection = document.querySelector('#places-list');
    if (!placesListSection) return;
    placesListSection.innerHTML = '';
    places.forEach(place => {
        const images = ['maison.jpg', 'maison2.jpg', 'maison3.jpg'];
        const randomImage = images[Math.floor(Math.random() * images.length)];
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');
        placeCard.innerHTML = `
            <div class="place-image-container">
                <img src="./images/${randomImage}" alt="${place.title}" class="place-image">
            </div>
            <div class="place-info">
                <h3 class="place-title">${place.title}</h3>
                <p class="place-price">Price per night: $${place.price}</p>
                <p class="place-location">Location: ${place.latitude}, ${place.longitude}</p>
                <button class="details-button" type="button" onclick="window.location.href='place.html?id=${place.id}';">View Details</button>
            </div>
        `;
        placesListSection.appendChild(placeCard);
    });
}


async function fetchPlaceDetails(placeId, token) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}


function displayPlaceDetails(place) {
    const placeDetailsSection = document.querySelector('#place-details');
    if (!placeDetailsSection) return;

    placeDetailsSection.innerHTML = `
        <h1>${place.title}</h1>
        <p><strong>Host:</strong> ${place.host}</p>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    if (token && placeId) {
        fetchPlaceDetails(placeId, token);
    }
});


// Fetch reviews for a specific place
async function fetchReviews(placeId, token) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
    }
}


// Dynamically display reviews
function displayReviews(reviews) {
    const reviewsSection = document.querySelector('#reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h2>Reviews:</h2>'; // Reset content
    reviews.forEach(review => {
        const reviewCard = document.createElement('article');
        reviewCard.classList.add('review-card');
        reviewCard.innerHTML = `
            <p><strong>${review.reviewer_name}:</strong></p>
            <p>"${review.text}"</p>
            <p>Rating: ${review.rating}/5</p>
        `;
        reviewsSection.appendChild(reviewCard);
    });
}


// Fetch reviews when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    if (token && placeId) {
        fetchReviews(placeId, token);
    }
});

// PART 4: ADD REVIEW - Get placeID from URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Function to submit a review to the API
// Submit a review dynamically
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            if (!token) {
                alert('You need to be logged in to submit a review.');
                window.location.href = 'login.html';
                return;
            }

            const reviewerName = document.getElementById('reviewer-name').value;
            const reviewText = document.getElementById('review-text').value;
            const rating = document.querySelector('.rating a:hover')?.getAttribute('href').substring(1) || 5;

            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ reviewer_name: reviewerName, text: reviewText, rating })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                    fetchReviews(placeId, token); // Refresh reviews
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting your review.');
            }
        });
    }
});
