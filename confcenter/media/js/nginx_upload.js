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

function fetch(uuid, loader) {
 req = new XMLHttpRequest();
 req.open("GET", url, 0);
 req.setRequestHeader("X-Progress-ID", uuid);
 req.onreadystatechange = function () {
  if (req.readyState == 4) {
   if (req.status == 200) {
    /* poor-man JSON parser */
    var upload = eval(req.responseText);

    //document.getElementById('tp').innerHTML = upload.state;
    progress = parseInt(upload.received) * 100 / parseInt(upload.size);
    /* change the width if the inner progress-bar */
    if (upload.state == 'done' || upload.state == 'uploading') {
	$( "#progressbar" ).progressbar({ value: progress });
	console.log(progress);
    }
    /* we are done, stop the interval */
    if (upload.state == 'done' || progress >= 100) {
	$( "#progressbar" ).hide();
       	$( "#analyze" ).show();
       	console.log("stopping");
	clearInterval(loader);
    }
   }
  }
 }
 req.send(null);
}

$(window).submit( function () {

    $( "#progressbar" ).progressbar({
        value: 0
    });
    $("#upload_form").attr("action","?X-Progress-ID=" + uuid);
    $( "#progressbar" ).fadeIn();
    $( "#progressbar" ).progressbar({ value: 0 });

    var loader = setInterval(function(){

	fetch(uuid, loader);

    }, 500);

});
