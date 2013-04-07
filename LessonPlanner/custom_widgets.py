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
	output = [u'<div>']
	# Normalize to strings
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
            rendered_cb = cb.render(name, option_value)
            option_label = "Title"
		
	    output.append("<li style='display:table-row'><div style='display: table-cell; vertical-align: middle'>%s </div>" % (rendered_cb))
	    output.append(u'<div style="display: table-cell"><label%s> <iframe width="200px" height="150px" temp="%s" src=""> </iframe></label></div></li>' % (label_for,  "http://www.youtube.com/embed/ImAMVqA6mug"))
#            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
	
        output.append(u'</div>')
#	print u'\n'.join(output)
        return mark_safe(u'\n'.join(output))
