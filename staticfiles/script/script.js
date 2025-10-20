document.addEventListener('DOMContentLoaded', function() {
    // Добавление обработчика для кнопки фильтрации
    const filterBtn = document.getElementById('filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', function(event) {
            event.preventDefault();
            let genre = document.getElementById('genre').value;
            let year = document.getElementById('year').value;
            let format = document.getElementById('format').value;
            let sortRating = document.getElementById('sort-rating').value;

            let url = new URL(window.location.href);
            if (genre) {
                url.searchParams.set('genre', genre);
            } else {
                url.searchParams.delete('genre');
            }
            if (year) {
                url.searchParams.set('year', year);
            } else {
                url.searchParams.delete('year');
            }
            if (format) {
                url.searchParams.set('format', format);
            } else {
                url.searchParams.delete('format');
            }
            if (sortRating) {
                url.searchParams.set('sort_rating', sortRating);
            } else {
                url.searchParams.delete('sort_rating');
            }

            window.location.href = url.href;
        });
    }

    // Добавление обработчиков для кнопок избранного
    const favoriteButtons = document.querySelectorAll('.favorite-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const animeId = this.getAttribute('data-anime-id');
            const icon = this.querySelector('i');
            const form = this.closest('form');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ anime_id: animeId })
            }).then(response => {
                return response.json();
            }).then(data => {
                if (data.is_favorite) {
                    icon.classList.remove('fa-star-o');
                    icon.classList.add('fa-star');
                } else {
                    icon.classList.remove('fa-star');
                    icon.classList.add('fa-star-o');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
            });
        });
    });

    // Обработчики для редактирования комментариев
    const editButtons = document.querySelectorAll('.edit-comment');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const commentText = document.querySelector(`.comment-text[data-comment-id="${commentId}"]`);
            const editForm = document.getElementById(`edit-form-${commentId}`);

            commentText.style.display = 'none';
            editForm.style.display = 'block';
        });
    });

    // Обработчики для сохранения изменений
    const saveEditButtons = document.querySelectorAll('.save-edit');
    saveEditButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const editForm = document.getElementById(`edit-form-${commentId}`);
            const textarea = editForm.querySelector('textarea');
            const newText = textarea.value;

            fetch(`/comments/edit/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: newText })
            }).then(response => {
                return response.json();
            }).then(data => {
                if (data.success) {
                    const commentText = document.querySelector(`.comment-text[data-comment-id="${commentId}"]`);
                    commentText.textContent = newText;
                    commentText.style.display = 'block';
                    editForm.style.display = 'none';
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while saving your comment. Please try again.');
            });
        });
    });

    // Обработчики для отмены редактирования
    const cancelEditButtons = document.querySelectorAll('.cancel-edit');
    cancelEditButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const commentText = document.querySelector(`.comment-text[data-comment-id="${commentId}"]`);
            const editForm = document.getElementById(`edit-form-${commentId}`);

            commentText.style.display = 'block';
            editForm.style.display = 'none';
        });
    });

    // Обработчики для удаления комментариев
    const deleteButtons = document.querySelectorAll('.delete-comment');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');

            fetch(`/comments/delete/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                return response.json();
            }).then(data => {
                if (data.success) {
                    const comment = document.getElementById(`comment-${commentId}`);
                    comment.remove();
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting your comment. Please try again.');
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Добавление обработчиков для кнопок удаления комментария
    const deleteButtons = document.querySelectorAll('.delete-comment');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            fetch(`/comments/delete/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.ok) {
                    document.getElementById(`comment-${commentId}`).remove();
                } else {
                    alert('An error occurred while deleting your comment. Please try again.');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting your comment. Please try again.');
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
