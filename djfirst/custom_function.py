from django.db.models import Q
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
# System Alert function used to write entries into session
# Developed By Neeraj Kumar : singhnk288@gmail.com
def pnotify(request,title = False, message = False, class_type = False):
	if title and message and class_type:
			# create variable which use to append pnotify session but
			# first check if already exists then append else add
			# type : success , warning , danger
			notify_data = request.session.get('pnotify',False)
			# loop for storing data as required
			iterate = 1		
			temp_data = {'title' : str(title),'message' : str(message), 'type' : str(class_type)}		
			if notify_data:			
				for data in notify_data:
					iterate = iterate + 1	
				# Append new Notify message		
				notify_data[iterate] = temp_data
			else:
				notify_data = {}
				notify_data[iterate] = temp_data				
			request.session['pnotify'] = notify_data				
			return notify_data
	else:
		return False

# sorting order accept default sorting value other this get from request parameter
# Developed By Neeraj Kumar : singhnk288@gmail.com
def sorting_order(request,sort_order = False):
	if sort_order:
		sort_by = request.GET.get('sort',sort_order)
		order_by = request.GET.get('order',False)		
		if order_by and order_by == 'desc':
			sort_by = '-'+ sort_by
		return sort_by
	else:
		return ''

# Transalation From One Language To Another 
# Function accept string and its return transalation string
# temporary disable because i dont thing this is best approach
def translate_string(string_value):
	return _(string_value)

# Convert List to Dict
def convert_List_Dict(lst): 
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
    return res_dct

# Check User Permision and raise exception according
def check_user_permission(request,app_name , permission_name):    
	# concatinate string with proper permision name
	if not request.user.has_perm(app_name+'.'+permission_name):
		raise PermissionDenied
	return True

# Server Error Pages : 500
def server_error(request):
    return render(request, 'errors/500.html')
 
# Page Not Found Error : 404 
def not_found(request,exception):    					  		    
	return render(request, 'errors/404.html')

# Permission Denied Error : 403
def permission_denied(request,exception):	    	
	data = {}	
	if request.data:    		
			data = request.data  	   
	return render(request, 'errors/403.html',data)

# Bad Request Error : 400
def bad_request(request,exception):
    return render(request, 'errors/400.html')
