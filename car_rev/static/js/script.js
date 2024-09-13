function submitComment() {
    const email = document.getElementById('email').value;
    const car = document.getElementById('car').value;
    const commentText = document.getElementById('comment').value;

    fetch('/api/comments/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            car: car,
            comment: commentText,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        fetchComments();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchComments() {
    fetch('/api/comments/')
    .then(response => response.json())
    .then(data => {
        const commentsDiv = document.getElementById('comments');
        commentsDiv.innerHTML = '';
        data.forEach(comment => {
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment';
            commentDiv.innerHTML = `
                <p><strong>Email:</strong> ${comment.email}</p>
                <p><strong>Car:</strong> ${comment.car_name}</p>
                <p><strong>Comment:</strong> ${comment.comment}</p>
            `;
            commentsDiv.appendChild(commentDiv);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

fetchComments();