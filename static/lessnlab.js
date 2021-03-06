var SITE = SITE || {};
 
SITE.fileInputs = function() {
  var $this = $(this),
      $val = $this.val(),
      valArray = $val.split('\\'),
      newVal = valArray[valArray.length-1],
      $button = $this.siblings('.button'),
      $fakeFile = $this.siblings('.file-holder');
  if(newVal !== '') {
    if($fakeFile.length === 0) {
      
    } else {
      $fakeFile.text(newVal);
    }
  }
};
 
$(document).ready(function() {
  $('.file-wrapper input[type=file]').bind('change focus click', SITE.fileInputs);
});
 
$(document).ready(function() {
  $('.file-wrapper input[type=file]')
  .bind('change focus click', SITE.fileInputs);
});




function goToByScroll(id){
	$('html,body').animate({scrollTop: $("#"+id).offset().top - 100},1500);
}
			
// Youtube and Video helper functions ///
function getVideoIDfromLink(url)
{
		var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
		var match = url.match(regExp);
		if (match&&match[2].length==11){
				return match[2];
		}else{
				//error
		}
};

function getVideoHtmlbyLink(video_link,div_id)
{
	video_id = getVideoIDfromLink(video_link);
	getVideoHtmlbyID(video_id,div_id);
};

function getVideoHtmlbyID(video_id,div_id)
{
	jQTubeUtil.video(video_id,function(response)
	{
		var video = response.videos[0];
		jQuery("#"+div_id).html(getVideoHtml(video));
	});
};
function actualNextSibling(el)
{    // needed to smooth out default firefox/IE behavior
	do { el = el.nextSibling } while (el && el.nodeType !== 1);
		return el;
};


function onVidImgClick(el)
{
	actualNextSibling(el).style.display='inline';
	el.style.display='none';
	var iframe = actualNextSibling(el).children[0];
	var url = iframe.getAttribute("temp");
	iframe.setAttribute("src",url);
	el.parentNode.style.width='600px';
	el.parentNode.children[0].style.display='none';
};

function getVideoHtml(video)
{
	var title = video.title.substring(0,32);
	var description = video.description.substring(0,32);
	var video_id = video.videoId;
	var url = "http://www.youtube.com/watch?feature=player_embedded&v=" + video_id;
	return "<div style='width:430px;'> <div style='width:275px; float:right'> " +
				"<b>Title: </b> <a href='" + url + "' > "  + title +
				"</a><div> <b> Description: </b>" + description +
				"</div> </div> <div onclick='onVidImgClick(this)' > " +
				"<img src='http://img.youtube.com/vi/" + video_id + "/1.jpg' alt='splash' width='120px' height='90px' style='cursor: pointer' style='display:inline'/ ></div> " +
				"<div style='display: none'>   <iframe width='300px' height='200px' temp='http://www.youtube.com/embed/" + video_id + "?autoplay=0&wmode=transparent'> </iframe></div>";

};
////////////////////////////////////////////////////////////////////////////////



//Full Screen////////////////////////////////////////////////////////////////
(function() {
    var
        fullScreenApi = {
            supportsFullScreen: false,
            isFullScreen: function() { return false; },
            requestFullScreen: function() {},
            cancelFullScreen: function() {},
            fullScreenEventName: '',
            prefix: ''
        },
        browserPrefixes = 'webkit moz o ms khtml'.split(' ');
 
    // check for native support
    if (typeof document.cancelFullScreen != 'undefined') {
        fullScreenApi.supportsFullScreen = true;
    } else {
        // check for fullscreen support by vendor prefix
        for (var i = 0, il = browserPrefixes.length; i < il; i++ ) {
            fullScreenApi.prefix = browserPrefixes[i];
 
            if (typeof document[fullScreenApi.prefix + 'CancelFullScreen' ] != 'undefined' ) {
                fullScreenApi.supportsFullScreen = true;
 
                break;
            }
        }
    }
 
    // update methods to do something useful
    if (fullScreenApi.supportsFullScreen) {
        fullScreenApi.fullScreenEventName = fullScreenApi.prefix + 'fullscreenchange';
 
        fullScreenApi.isFullScreen = function() {
            switch (this.prefix) {
                case '':
                    return document.fullScreen;
                case 'webkit':
                    return document.webkitIsFullScreen;
                default:
                    return document[this.prefix + 'FullScreen'];
            }
        }
        fullScreenApi.requestFullScreen = function(el) {
            return (this.prefix === '') ? el.requestFullScreen() : el[this.prefix + 'RequestFullScreen']();
        }
        fullScreenApi.cancelFullScreen = function(el) {
            return (this.prefix === '') ? document.cancelFullScreen() : document[this.prefix + 'CancelFullScreen']();
        }
    }
 
    // jQuery plugin
    if (typeof jQuery != 'undefined') {
        jQuery.fn.requestFullScreen = function() {
 
            return this.each(function() {
                if (fullScreenApi.supportsFullScreen) {
                    fullScreenApi.requestFullScreen(this);
                }
            });
        };
    }
 
    // export api
    window.fullScreenApi = fullScreenApi;
})();

//MODIFIED ajax send to make ajax calls work b/c of CRSF tokens //////////

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
////////////////////////////////////////////////////////////////
