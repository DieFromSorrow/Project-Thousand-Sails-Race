
function AJAX_send(url, func) {
    $.ajax({
        url: url,
        type: 'get',
        success: function(data) {
            func(data)
        }
    })
}

