function createForm(myData) {
	
	var htmlString = "hello <br/>"
	var count=0;
        for (var f in myData) {	
		htmlString += "<form name=input id=" + count + ">"
		contentSection = myData[f]['fields'];
		htmlString += "<input type=\"text\" value=" + contentSection['SectionNumber'] + ">";
		htmlString += "<input type=\"text\" value=" + contentSection['Header'] + ">";
		htmlString += "<input type=\"text\" value=\"" + contentSection['Content'] + "\">";
		htmlString += "</form>"
	}
	return htmlString;

}

$(document).ready(function() {
    $( ".l").each(function() {
        $(this).click(function() {
                var id = $(this).attr('lID');
                $.post("/lessons/", {
                    lID:id ,
                 },
	    		function(data) {
				try{
				if(data == "") {
					$('#cont').html("")
					return;
				}
				
				var myData = jQuery.parseJSON(data)
				alert (myData)
				var htmlString = '';
				$.each(myData,function(){
					htmlString += this['fields']['Content'] + "<br/>"
				});
				$('#cont').html(createForm(myData));
                		cont = myData;
				}
				catch (e) {
					alert(e);
				}
            		}
	    	);
		
       } );
    })
});



