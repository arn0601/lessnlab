from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms.util import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import conditional_escape
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils import datetime_safe, formats, six
from django import forms


def format_html(format_string, *args, **kwargs):
    """
    Similar to str.format, but passes all arguments through conditional_escape,
    and calls 'mark_safe' on the result. This function should be used instead
    of str.format or % interpolation to build up small HTML fragments.
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = dict([(k, conditional_escape(v)) for (k, v) in
                        six.iteritems(kwargs)])
    return mark_safe(format_string.format(*args, **kwargs))


class CalendarDateSelectField(forms.TextInput):
    def render(self, name, value, ulattrs=None, attrs=None, choices=()):
	if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html(u'<input{0} />', flatatt(final_attrs))
