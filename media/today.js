// today.js
$(document).ready(function() {
    $('#yesterday').click(function() {
        $.post("/today/", {
            today: today,
            },

            function(data) {
                $('#date').html(data);
                today = data;
            }
        );
    });
});
