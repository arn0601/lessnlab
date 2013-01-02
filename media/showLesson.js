
function saveSection(lid, formname) {
	try {
	alert(formname)
	var form = document.forms[formname];
	var sectionNumber = form["secnum"].value;
	var header = form["header"].value;
	var content = form["content"].value;
	var section = new Object()
	section.sectionNumber=sectionNumber;
	section.header=header;
	section.content=content;
	var secstring = JSON.stringify(section);
	$.post("/lessons/", { action:1, lID:lid, section:secstring }, showLesson(lid));
	} catch(e) { alert(e) }
}
function createForm(myData, lid) {
	
	var htmlString = "hello <br/>"
	var count=0;
        for (var f in myData) {	
		contentSection = myData[f]['fields'];
		htmlString += "<form name=input" + contentSection['SectionNumber'] + " method=\"post\" onsubmit=\"return saveSection(" + lid + ",'input" + contentSection['SectionNumber'] + "')\">";
		htmlString += "<input name=secnum type=\"text\" value=" + contentSection['SectionNumber'] + ">";
		htmlString += "<input name=header type=\"text\" value=" + contentSection['Header'] + ">";
		htmlString += "<input name=content type=\"text\" value=\"" + contentSection['Content'] + "\">";
		htmlString += "<input type=\"submit\" value=\"submit\">"
		htmlString += "</form>"
	}
	return htmlString;

}

function showLesson(id) {

                $.post("/lessons/", {
                    lID:id , action:0,
                 },
                        function(data) {
                                try{
                                if(data == "") {
                                        $('#cont').html("")
                                        return;
                                }

                                var myData = jQuery.parseJSON(data)
                                var htmlString = '';
                                $.each(myData,function(){
                                        htmlString += this['fields']['Content'] + "<br/>"
                                });
                                $('#cont').html(createForm(myData, id));
                                cont = myData;
                                }
                                catch (e) {
                                        alert(e);
                                }
                        }
                );


}

$(document).ready(function() {
    $( ".l").each(function() {
        $(this).click(function() {
                var id = $(this).attr('lID');
                $.post("/lessons/", {
                    lID:id , action:0, 
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
				$('#cont').html(createForm(myData, id));
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



