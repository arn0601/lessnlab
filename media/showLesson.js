$(document).ready(function() {
    $( ".l").each(function() {
        $(this).click(function() {
                var id = $(this).attr('lID');
                $.post("/lessons/", {
                    lID:id ,
                 },
	    		function(data) {
				if(data == "") {
					$('#cont').html("")
					return;
				}
				var myData = eval("(" + data + ")");
				var htmlString = '';
				$.each(myData,function(){
					htmlString += this['fields']['Content'] + "<br/>"
				});
				$('#cont').html(htmlString);
                		cont = myData;
            		}
	    	);
		
       } );
    })
});
