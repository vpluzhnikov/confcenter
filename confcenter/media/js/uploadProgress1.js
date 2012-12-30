//to generate uuid
function genUUID() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid;
};

//to update progress info
function updateProgressInfo() {
    var progress_url = "/upload/progress/"; // ajax view serving progress info
    var uuid = $('#X-Progress-ID').val();
//    $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
//        if (data) {
//             uncomment to check in firebug
//            console.log("uploaded: " + data.uploaded);
//            var progress = parseInt(data.uploaded) * 100 / parseInt(data.length);
//            $("#upload-progress-bar").progressBar(progress);
//            trigger the next one after 1s
//            $("#upload-progress-bar").oneTime(1000, function() {
//                updateProgressInfo();
//            });
//        }
//    });
};

// pre-submit callback
function beforeSubmitHandler(formData, jqForm, options) {
    $("#upload-progress-bar").fadeIn();
    $("#upload-progress-bar").progressBar({
        boxImage: '/media/upload/img/progressbar/ajax-loader.gif'
//        barImage: '{{ STATIC_URL }}img/progressbar/progressbg_orange.gif'
    });
    // trigger the 1st one

    $("#upload-progress-bar").oneTime(1000, function(){
        updateProgressInfo();
    });

    return true;
};

// post-submit callback
function successHandler(responseText, statusText, xhr, $form) {
    alert("Sucsses");
//    delay and redirect the page to somewhere else
//    $("#upload-file-form").oneTime(1000, function() {
//        {% url tracefiles-root as tracefiles_root_url %}
//        window.location.replace("{{ tracefiles_root_url }}process/");
//    });
//
    return true;
};

// on page load
$(function() {
    alert("Started");
    var uuid = genUUID(); // id for this upload so we can fetch progress info.
//    save the uuid with the element
//    $('#X-Progress-ID').val(uuid);
    var options = {
        dataType: "xml",
        url: "/upload/progress/?X-Progress-ID="+$('#X-Progress-ID').val(),
        beforeSubmit: beforeSubmitHandler,
        success: successHandler
    };
    $("#upload-file-form").ajaxForm(options);
})
