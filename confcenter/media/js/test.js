var base_url = "http://127.0.0.1:8000"
var url = "/upload/progress/"


//$.ajax({
//    type: "GET",
//    url: "http://127.0.0.1:8000/upload/progress",
//    dataType: "json",
//    data: { "X-Progress-ID" : uuid },
//    success: function(data) {
//        $( "#progressbar" ).progressbar({ value: 70 });
//        alert("succsess");
//    },
//    error: function(data) {
//        $( "#progressbar").progressbar({ value: 20});
//        alert("succsess");
//    }
//});

function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid;
}

$(window).submit(function () {

    var uuid = gen_uuid();

    $( "#progressbar" ).progressbar({
        value: 0
    });
    $("#upload_form").attr("action","?X-Progress-ID=" + uuid);
    $( "#progressbar" ).fadeIn();
    $( "#progressbar" ).progressbar({ value: 0 });


    var loader = setInterval(function(){

        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/upload/progress",
            dataType: "json",
            data: { "X-Progress-ID" : uuid },
            success: function(data) {
//                $( "#progressbar" ).progressbar({ value: 70 });
//                alert("succsess");
                var progress = parseInt(data.uploaded) * 100 / parseInt(data.length);
                console.log("Progress: " + progress);
                $( "#progressbar" ).progressbar({ value: progress });
//                $("#upload-progress-bar").progressBar(progress);

            },
            error: function(data) {
                $( "#progressbar").progressbar({ value: 20});
//                alert("error");
            }
        });


    }, 500);

//        var jsonreq = $.getJSON(base_url + url, {'X-Progress-ID' : uuid}, function(){
//            alert("succsess");
//        })
//        $.ajax({
//            type: "GET",
//            url: base_url + url,
//            dataType: "json",
//            success: function() {
//                $( "#progressbar" ).progressbar({ value: 50 });
//            },
//            error: function() {
//                $( "#progressbar").progressbar({ value: 20});
//            }
//        });
})
