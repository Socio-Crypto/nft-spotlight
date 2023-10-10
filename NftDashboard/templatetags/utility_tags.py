from django import template
from datetime import datetime
register = template.Library()

@register.filter
def get_date(date):
    from datetime import datetime
    diff_date = (datetime.today() - datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')).days
    text = 'days ago'
    if diff_date > 365:
        diff_date = round(diff_date /365)
        text = 'years ago'
    elif diff_date > 30:
        diff_date = round(diff_date/30)
        text = 'months ago'
    
    
    return(str(diff_date) + ' ' + text) 

@register.simple_tag
def get_feature(dictionary, key, value):
    return round(dictionary[key][value],1)