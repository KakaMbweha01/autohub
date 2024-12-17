document.addEventListener('DOMContentLoaded', () => {
    const favoriteButtons = document.querySelectorAll('.togle-favorite');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const carId = button.getAttribute('data-car-id');
            const url = `/toggle-favorite/${carId}/`;

            fetch(url, { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrftoken') } })
            .then(response => response.json())
            .then(data => {
                if (data.favorited) {
                    button.textContent = 'Unfavorite';
                } else {
                    button.textContent = 'Favorite';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Function to get CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});