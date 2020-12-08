const user_input = $("#user-input")
const search_icon = $('#search-icon')
const questions_div = $('#replaceable-content')
const endpoint = '/search/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            
            questions_div.fadeTo('slow', 0).promise().then(() => {
                
                questions_div.html(response['html_from_view'])
                
                questions_div.fadeTo('slow', 1)
                
                search_icon.removeClass('blink')
            })
        })
}


user_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() 
    }

    
    search_icon.addClass('blink')

    
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})