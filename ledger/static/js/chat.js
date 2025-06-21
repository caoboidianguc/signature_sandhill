

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0 ; i < cookies.length; i++ ) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length +1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length +1 ));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    

    $(document).ready(function() {
        $('.like-button').on('click', function() {
            const button = $(this);
            const url = button.data('url');
            $.ajax({
                url: url,
                type: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    if (data.liked) {
                        button.addClass('liked');
                        button.closest('div').find('.chat-text').removeClass('fw-bold'); //can't use button.closest('a') cause a and p is subbling, it not work
                    } else {
                        button.removeClass('liked');
                    }
                    button.closest('p').find('.like-count').text(data.total_likes);
                },
                error: function(xhr, status, error) {
                    console.log('Error', error);
                    alert('Failed to update like. Please try again.');
                }
            });
        });
    });

    $(document).ready(function() {
        $('.delete-chat').on('click', function() {
            const button = $(this);
            const chatId = button.attr('data-chat-id');
            const url = button.data('url');
            $.ajax({
                url: url,
                type: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {
                    if (data.success){
                        button.closest('div').remove();
                        alert("Your post was delete");
                    } else {
                        alert("Can't delete this post" + data.error);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log('Error', jqXHR.responseText, textStatus, errorThrown);
                    alert("Can't delete this post" + textStatus);
                }
            });
        });
    });

    