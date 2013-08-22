
$(document).ready(function(){
	$('.editabletextarea').click(function(){
			$(this).hide();
			var div = $('<textarea wrap="soft">' + $.trim($(this).html()) + '</textarea>');
			var attributes = $(this).prop("attributes");
			// loop through <select> attributes and apply them on <div>
			$.each(attributes, function() {
					if (this.name != "class")
						div.attr(this.name, this.value);
			});
			
			div.insertAfter($(this));
			$(this).next().show();
			$(this).next().select();
	});
	
	$('.editabletext').click(function(){
			$(this).hide();
		  
			var div = $('<input type="text" value="' + $.trim($(this).html()) + '" />');
			var attributes = $(this).prop("attributes");
			// loop through <select> attributes and apply them on <div>
			$.each(attributes, function() {
					div.attr(this.name, this.value);
			})
			
			div.insertAfter($(this));
			$(this).next().show();
			$(this).next().select();
	});
		
	$(function(){
	$(document).on('blur', 'textarea', function(e){ 
		if ($.trim(this.value) == ''){  
		 this.value = (this.defaultValue ? this.defaultValue : '');  
		}
		else{
		 $(this).prev().html(this.value);
		}
	
		$(this).prev().show();
		try{
			var url = $(this).attr('url');
			var model_map_id = $(this).attr('model_map_id');
			var objid = $(this).attr('obj_id');
			var t = setData(model_map_id, objid, this.value, url );
			$(this).remove()
		}
		catch(err)
		{
			
		}
	});
	});
		
	$(function(){
	$(document).on('blur', 'input[type="text"]', function(e){ 
		if ($.trim(this.value) == ''){  
		 this.value = (this.defaultValue ? this.defaultValue : '');  
		}
		else{
		 $(this).prev().html(this.value);
		}
		$(this).prev().show();
		
		try{
			var url = $(this).attr('url');
			var model_map_id = $(this).attr('model_map_id');
			var objid = $(this).attr('obj_id');
			var t = setData(model_map_id, objid, this.value, url )
			$(this).remove()
		}
		catch(err)
		{
			
		}
	});
	});
		

			
	$(function(){
		$(document).on('keypress', 'input[type="text"]', function(event){
			if (event.keyCode == '13') {
				if ($.trim(this.value) == ''){  
					this.value = (this.defaultValue ? this.defaultValue : '');  
				}
				else{
				 $(this).prev().html(this.value);
				}
				$(this).prev().show();
		
				try{
					var url = $(this).attr('url');
					var model_map_id = $(this).attr('model_map_id');
					var objid = $(this).attr('obj_id');
					var t = setData(model_map_id, objid, this.value, url )
					$(this).remove()
				}
				catch(err)
				{
					
				}
			}
		});
	});
	
	function setData(model_map_id, obj_id, value, urlvar) {
		$.ajax({ // create an AJAX call...
			data: {
				model_map_id : model_map_id,
				obj_id : obj_id,
				value : value,
			},
			type: "POST", // GET or POST
			url: urlvar,
			success: function(response) { // on success..
				return response;
			}
		});
	}	
	
	
});