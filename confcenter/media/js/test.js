function updateProgressInfo() {
    $( "#progressbar").progressbar({ value: 50 });
//var progress_url = "/upload/progress/"; // ajax view serving progress info
//var uuid = $('#X-Progress-ID').val();
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

$(document).submit(function () {
    alert("test");

    $( "#progressbar" ).progressbar({
        value: 0
    });
    var loader = self.setInterval(updateProgressInfo,500);

})
