$(window).on('load', function() {
    $('#loading').hide();
});
$(window).bind('beforeunload', function(){
    $('#loading').show();
});
function injectMessage(msg, color = 'success') {
    var toastString = '<div class="toast d-flex align-items-center  bg-{{color}} mx-5 my-2" role="alert" id="toast"'
        + 'aria-live="assertive" aria-atomic="true">'
        + '<div class="toast-body"></div>'
        + '<button type="button" class="btn-close btn-close-white ms-auto me-2" data-bs-dismiss="toast" aria-label="Close"></button>'
        + '</div>';

    toastString = toastString.replace('{{color}}', color);
    var toastHtml = $.parseHTML(toastString)[0];

    messageContainer = $('#message-container');
    $(toastHtml).find('.toast-body').html(msg)
    messageContainer.html('');
    messageContainer.append($(toastHtml));
    toast = new bootstrap.Toast(toastHtml)
    toast.show();
}

$("#clickme").click(function () {
    $("#guideshow").fadeToggle();
    // $( "#guideshow" ).toggle({ direction: "left" }, 1000);
});

// $("#clickme").hover(function(){
//     $("#guideshow").slideUp('slow');
// }, function(){
//     $("#guideshow").slideToggle('slow');
// });
