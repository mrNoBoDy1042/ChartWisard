document.getElementById('submit-button').addEventListener('click', function(e) {
    e.preventDefault();

    var database = document.getElementById('database').value;
    var question = document.getElementById('question').value;

    var request = {
        database: database,
        question: question
    };

    // Create a new loader and backdrop
    var loader = document.createElement('div');
    loader.className = 'loader';

    var loaderBackdrop = document.createElement('div');
    loaderBackdrop.className = 'loader-backdrop';
    loaderBackdrop.appendChild(loader);

    // Append the loader and backdrop to the body
    document.body.appendChild(loaderBackdrop);

    fetch('/api/question/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(data => {
        // Remove the loader and backdrop
        document.body.removeChild(loaderBackdrop);

        if (data && data.query) {
            window.location.href = '/results?query=' + encodeURIComponent(data.query);
        } else {
            alert('There was an error processing your request. Please try again.');
        }
    })
    .catch((error) => {
        // Remove the loader and backdrop in case of error
        document.body.removeChild(loaderBackdrop);
        console.error('Error:', error);
    });
});
