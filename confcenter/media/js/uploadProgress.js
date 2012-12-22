function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid
}

// Add upload progress for multipart forms.
$(function() {
    $().submit(function(){
//        if ($.data(this, 'submitted')) return false;

        alert("Submitting")

        $("#upload-progress-bar").fadeIn();
        $("#upload-progress-bar").progressBar({
//            boxImage: '/media/upload/img/progressbar/ajax-loader.gif'
//        barImage: '{{ STATIC_URL }}img/progressbar/progressbg_orange.gif'
//        });
        // trigger the 1st one
//        $("#upload-progress-bar").oneTime(1000, function(){
//            updateProgressInfo();
//        });



//        $.data(this, 'submitted', true); // mark form as submitted.
    })
});