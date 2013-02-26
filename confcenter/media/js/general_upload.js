var url = "/upload/progress/"


var uuid = gen_uuid();
$.ajaxSetup({
    async: false
});

function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid;
}
$(window).submit( function () {

    $( "#progressbar" ).progressbar({
        value: 0
    });
    $("#upload_form").attr("action","?X-Progress-ID=" + uuid);
    $( "#progressbar" ).fadeIn();
    $( "#progressbar" ).progressbar({ value: 0 });

    var loader = setInterval(function(){

        $.getJSON(url, {"X-Progress-ID" : uuid}, function(data, status){
                var progress = 0
		if (parseInt(data.size) > 0) {
		    progress = parseInt(data.received) * 100 / parseInt(data.size);
		}
                console.log("Progress: " + progress);
                if (progress < 100){
                    $( "#progressbar" ).progressbar({ value: progress });
                    console.log(progress);
                }
                else {
                    $( "#progressbar" ).progressbar({ value: progress });
                    $( "#progressbar" ).hide();
                    $( "#analyze" ).show();
                    console.log("stopping");
                    clearInterval(loader);
                }
        });

    }, 500);

});
