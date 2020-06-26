from django import template
# Import required library
from cms_master.models import *
from django.utils.translation import get_language
register = template.Library()

# This function use to retreive dictionary value
@register.filter(name="get_item_value")
def get_item_value(dictionary = False, key = False):    
    if not (dictionary or key):
        return False
    try:
        string = dictionary.get(key)
        return string
    except:
        return False

# Convert List to Dict then inside multi dict convert to single dict
@register.filter(name = "convert_list_dict")
def convert_list_dict(lst,language_code):       
    if lst:
        # it = iter(lst) 
        # temp_dict = dict(zip(it, it)) 
        # # temp_dict = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
        # print(temp_dict)
        # multi dict convert to single dict
        single_temp_dict = dict()
        for item in lst:            
            single_temp_dict.update(eval(item))
        try:
            country = single_temp_dict.get(language_code)
            return country
        except:
            return False
    return False

@register.filter(name = "get_country_name_by_id")
def get_country_name_by_id(country_id):    
    if country_id:               
        country_obj = CountryMappingLanguage.objects.filter(country_foriegn_id = country_id,langauge__code = get_language()).first()        
        if country_obj:
            return country_obj
        else:
            return 'NA'
    else:
        # Na if no data found
        return 'NA'

@register.filter()
def to_int(value):
    return int(value)
