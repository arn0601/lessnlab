$(document).ready(function() {
    $( ".l").each(function() {
        $(this).click(function() {
                var id = $(this).attr('lID');
                $.post("/lessons/", {
                    lID:id ,
                 },
	    		function(data) {
				var myData = eval("(" + data + ")");
				var htmlString = '';
				$.each(myData,function(){
					htmlString += this['fields']['Content'] + "<br/>"
				});
				$('#cont12').html(htmlString);
                		cont = myData;
            		}
	    	);
		
       } );
    })
});
