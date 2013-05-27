from django import template
register = template.Library()

@register.filter(name='isdict')
def isdict(value):
	if isinstance(value, dict):
		return 'T'
	return 'F'

@register.filter(name='access')
def access(value, arg):
	print value
	print arg
	if isinstance(value.get(arg),dict):
		new_dict = {}
		for key in value[arg].keys():
			new_dict[key] = value[arg][key]
		return new_dict
	
	return value.get(arg)

@register.filter(name='sort_placement')
def sort_placement(value):
        l = []
        for key in value:
                l.append((key, key.placement))
        l.sort(key=lambda x: x[1])
        return  l
