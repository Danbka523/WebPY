from django import template
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter(name='newline_to_br') 
def newline_to_br(value):
    return value.replace('\n', '<br>')
