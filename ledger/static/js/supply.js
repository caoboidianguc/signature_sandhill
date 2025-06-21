
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

$(document).ready(function(){
    $('.nut-item').on('click', function() {
        const button = $(this);
        const itemId = button.attr('data-item-id');
        const supplyUrl = button.data('url');
        $.ajax({
            url: supplyUrl,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(data) {
                if (data.success) {
                    if (data.is_wanted) {
                        button.addClass('fs-2 text-success');
                        button.find('.add-cart').html('<i class="bi bi-bag-check"></i>');
                        button.find('.item-time').remove();
                    } else {
                        button.removeClass('fs-2 text-success');
                        button.find('.add-cart').html('');
                    }
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(xhr.responseJSON.error);
                } else {
                    alert("Can't turn priority");
                }
            }
        });
    });

    let showDelete = false;
    
    if (!showDelete){
        $('.delete-item').hide()
    }
    $('.edit-supply').on('click', function() {
        showDelete = !showDelete;
        
        if (showDelete) {
            $('.delete-item').show();
            $(this).find('i').addClass('text-danger');
        } else {
            $('.delete-item').hide();
            $(this).find('i').removeClass('text-danger');
        }
    });

    $('.delete-item').on('click', function() {
        const nutXoa = $(this);
        const urlSupply = nutXoa.data('url');
        $.ajax({
            url: urlSupply,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(data) {
                if (data.success) {
                    nutXoa.closest('li').remove();
                    alert('Item removed from data');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Can't remove item yet.")
            }
        });
    });

});
