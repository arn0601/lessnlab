// today.js
$(document).ready(function() {
    $('#lesson').click(function() {
        var id = $(this).attr('lID');
	alert("HELLO")
	$.post("/lessons/", {
            lID:id ,
            },

        );
    });
});


