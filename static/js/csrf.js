// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up CSRF token for all AJAX requests
$(document).ready(function() {
    const csrftoken = getCookie('csrftoken');
    
    // Set up AJAX to always send CSRF token
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    // Ensure CSRF token is correctly passed with all forms
    $('form').each(function() {
        const form = $(this);
        if (!form.find('input[name="csrfmiddlewaretoken"]').length) {
            form.append(`<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">`);
        }
    });
}); 