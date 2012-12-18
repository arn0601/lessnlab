$(document).ready(function() {
    $( ".l").each(function() {
        $(this).click(function() {
                var id = $(this).attr('lID');
                $.post("/lessons/", {
                    lID:id ,
                 },
	    		function(data) {
				$('#cont').html(data);
                		cont = data;
            		}
	    	);
		
       } );
    })
});
