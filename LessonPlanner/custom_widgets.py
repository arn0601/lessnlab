from django import forms
from LessonPlanner.models import *
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, ulattrs=None, attrs=None, choices=()):
	print value,name        
	if value is None: value = []
	has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
	final_attrs["style"]="margin-right:10px"
	output = [u'<div> ']
	output.append(u'<div class="span5 noborderunitbox" style="float:left">')
	output.append(u'Recommended Videos:')
  	str_values = set([force_unicode(v) for v in value])
#	print "chocies",choices,"asd",self.choices
	for i, (option_value, option_label) in enumerate(self.choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = option_value
            rendered_cb = cb.render(name, option_label)
	    url = option_label	
	    output.append("<li style='display:table-row'><div style='display: table-cell; vertical-align: middle'>%s </div>" % (rendered_cb))
	    vid_html = '''<div style='margin-bottom:10px' id='rec''' + str(i) + ''''>
				<script type='text/javascript'>
					document.getElementById('rec''' + str(i) + '''').innerHTML = getVideoHtmlbyLink("''' + url +  '''",'rec'''+str(i)+'''');
				</script>
			</div></li>'''
	    output.append(vid_html)
	    
# output.append(u'<div style="display: table-cell"><label%s> <iframe width="200px" height="150px" temp="%s" src=""> </iframe></label></div></li>' % (label_for,  "http://www.youtube.com/embed/ImAMVqA6mug"))

	output.append(u'</div>')
	output.append(u'<div class="span6 noborderunitbox" style="float:right">')
	output.append(u'Search Youtube:')
	html = '''
<div>
<input style=" display:inline-block; width:150px" type="text" name="free_text_1">
<button type="button" class="btn btn-primary" onclick="doBasicSearch();" style="
  margin-bottom:10px;">
				Search
</div>
<div id="basic_search_response_processing" class="inline-notifier" 					style="display: none;">				<img src="/images/loader.gif">
		</div>
		</button>

<div class="example_result">
	<div id="basic_search_response"></div>
</div>'''

	output.append(html)
  	output.append(u'</div>')
	output.append(u'</div>')
	return mark_safe(u'\n'.join(output))
