// Handles login page client side logic

$(function() {
    var username = $.cookie('username');
    var password = $.cookie('password');
    
    // restore field values, if available
    if (username) {
        $('[name=email]').val(username);
        $('[name=password]').val(password);
                
        $('#remember_me').get(0).checked = true;
    }
});