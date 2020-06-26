from django.shortcuts import render
from djfirst.custom_function import *
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.auth.models import *
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
from django.http import HttpResponseRedirect

# Temperatory HttpImport for debug
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# Define Custom model app name so if any change need you can directly from this global name
Model_App_Name = 'auth'

# Create your views here.
def user_login(request):
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # Redirect to home page : page show after login but
    # if you trying to access other required page without login
    # then after login page redirect to that particular page
    next_url = request.GET.get('next',False)
    if next_url:
        response = redirect(next_url)
    else:
        response = redirect('/master/language')   
    print(next_url)
    # check if user already login and they again trying to login then system not allow
    # redirect page to home page
    if request.user.is_authenticated:
        # Redirect to home page : page show after login        
        return response
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            pnotify(request,'User','Login Successfully','success')  
            print(response)                          
            return response
        else:
            data['pnotify'] = pnotify(request,'Login Failed','Username and Password not valid','danger')
    return render(request,'account/login.html',data)

@login_required
def user_logout(request):
    logout(request)
    pnotify(request,_('User'),_('Logout Successfully'),'success')
    response = redirect(settings.LOGIN_URL)
    return response

# View User Listing Page
@login_required
# @permission_required('auth.view_user')
def view_user(request):
    # Check Required Permission : Just add below line to validate permission : view user permission
    check_user_permission(request,Model_App_Name,'view_user')  
    
    data = request.data    
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    
    # set default page
    page_num = request.page_num
    # default sort order
    sort_order = sorting_order(request,'id')
    # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
    # if url variable not set then achor tag not set except when is_icon set url field is mandatory
    # active is used for not clickable breadcrumbs
    data['breadcrumbs'] = {
            _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
            _('User') : {'active' : True}
    }
    data['title'] = _('Master - User')
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('Add User') : {'url' : '/accounts/user/add/' , 'icon' : 'icon-add text-primary'},        
    }

    # Check Post Method is Call or not
    filter_array = {} # default value
    filter_form = {}
    # Handle Post method    
    if request.method == "POST":
        # Filter Button         
        if request.POST.get("filter") and request.POST.get("filter") == 'Filter': 
            search_key = request.POST.get('search','')
            # Check If Search Key not empty
            if search_key:
                # icontains use like %name%
                # user search from user name , first name , last name , email
                # filter_array = get_query(search_key,['username','email','first_name','last_name'])
                filter_array = {'username__icontains' : search_key,
                        'email__icontains' : search_key,
                        'first_name__icontains' : search_key,
                        'last_name__icontains' : search_key,
                        'groups__name__icontains' : search_key,
                         }                                
                filter_form['name'] = search_key
            request.session['user_master_conditions'] = filter_array
            request.session['user_master_form_data'] = filter_form
        # Reset all existing session and form data
        elif request.POST.get('reset') and request.POST.get('reset') == 'Reset':
            request.session['user_master_conditions'] = {}  
            request.session['user_master_form_data'] = {}      
    # Form Persistence : form data send into template
    filter_array = request.session.get('user_master_conditions',{})    
    filter_form = request.session.get('user_master_form_data',{})
    # Q object is used to create complex query    
    filter_string = Q()    
    for item in filter_array:
        filter_string |= Q(**{item:filter_array[item]})
    # pass data into template for 
    data['filter_form'] = filter_form    
    # create Object of data model
    results_obj = User.objects.all().filter(filter_string).order_by(sort_order);
    # find record by number of listing as you required per page
    paginator = Paginator(results_obj,request.pagination_record)
    total_result_count = paginator.count    
    # get result of a particualar page number
    results = paginator.get_page(page_num)  
    # send result to template  
    data['results'] = results    
    # send total count of record in django template
    data['total_result_count'] = total_result_count
    # Page listing count send into template
    data['listing_count'] = request.pagination_record
    return render(request,'authenticate/user.html',data)

# Add User From Master
@login_required
def add_user(request,id = '0'):
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View User') : {'url' : '/accounts/user' , 'icon' : 'icon-add text-primary'},        
    }    
    # create Object of data model - of Group Master
    filter_status = {'status':True}
    # All group listing in select box
    data['group_obj'] = Group.objects.all().filter(**filter_status).order_by('name')    
    # check whether this is new entries or update existing entries
    if id != '0':        
        # If User not have permission to change user and user want to change own profile then we allow to the same user
        if not request.user.has_perm(Model_App_Name+'.change_user') and request.user.id == int(id):
            data['current_user_allow_permission'] = True
        else:
            # Check Required Permission : Just add below line to validate permission : change user permission
            check_user_permission(request,Model_App_Name,'change_user')            
        # form persistence
        try:
            data['user_obj'] = User.objects.get(id = id)
        except:
            data['user_obj'] = False
        # If no data found that means either wrong id pass or
        #  record not found than redirect page to view page
        if not data['user_obj']:
            pnotify(request,'Master : User','User id invalid','danger')
            response = redirect('/accounts/user/')
            return response
        # Form Persistence current user group -> Group list in select box
        data['user_group_id'] = data['user_obj'].groups.values_list('id', flat=True).first()
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('User') : {'url' : '/accounts/user/'},
                _('Edit User') : {'active' : True}
        }
        data['title'] = _('Master - Edit User')
    else:
        # Check Required Permission : Just add below line to validate permission : add user permission
        check_user_permission(request,Model_App_Name,'add_user')
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('User') : {'url' : '/accounts/user/'},
                _('Add User') : {'active' : True}
        }
        data['title'] = _('Master - Add User')   
        
    # Handle Post method 
    if request.method == "POST":
        post_data = request.POST
        post_first_name = post_data.get('first_name')
        post_last_name = post_data.get('last_name')
        post_email = post_data.get('email')
        post_username = post_data.get('username')
        post_password = post_data.get('password')
        post_group_id = post_data.get('group_name')        
        # create post group object so we update group id
        post_group_obj = Group.objects.get(id = post_group_id)
        # In case of new entries
        if id == '0' :
            # Check duplicate user validation            
            record_exists = User.objects.filter(Q(username__iexact = post_username.strip()) | Q(email__iexact = post_email.strip())).count()
            # No Record Found            
            if record_exists == 0:                
                # parameter order : username , email , is_active default set as true
                user_obj = User.objects.create_user(post_username,post_email,post_password)
                user_obj.is_active = True
                user_obj.first_name = post_first_name
                user_obj.last_name = post_last_name
                user_obj.groups.set([post_group_obj])
                user_obj.save()
                data['pnotify'] = pnotify(request,_('Master : User'),_('New User Registered Successfully'),'success')
                return redirect('/accounts/user/')
            else:
                # Through Error      
                data['pnotify'] = pnotify(request,_('Master : User'),_('Username or Email Already Exists'),'danger')
                data['post_first_name'] = post_first_name
                data['post_last_name'] = post_last_name
                data['post_email'] = post_email
                data['post_username'] = post_username
                data['user_group_id'] = post_group_id
        else:
            # In Case of updation Record
            # Check duplicate user validation            
            record_exists = User.objects.filter(Q(username__iexact = post_username.strip())).exclude(id = id).count()
            # No Record Found            
            if record_exists == 0:
                try:
                    user_obj = User.objects.get(id = id)
                    error_status = True
                except:
                    error_status = False
                    data['pnotify'] = pnotify(request,_('Master : User'),_('User id not found'),'danger')
                if error_status:
                    user_obj.username = post_username
                    user_obj.first_name = post_first_name
                    user_obj.last_name = post_last_name
                    user_obj.groups.set([post_group_obj])
                    if post_password:
                        user_obj.set_password(post_password)
                    # Update Record
                    user_obj.save()
                    data['pnotify'] = pnotify(request,_('Master : User'),_('Edit User Saved Successfully'),'success')
                    return redirect('/accounts/user/')
            else:
                # Through Error
                data['pnotify'] = pnotify(request,_('Master : User'),_('Username or Email Already Exists'),'danger')                
                data['post_first_name'] = post_first_name
                data['post_last_name'] = post_last_name
                data['post_email'] = post_email
                data['post_username'] = post_username
                data['user_group_id'] = post_group_id    
    return render(request,'authenticate/add_user.html',data)

# Master function for view language
@login_required
def view_group(request):  
    # Check Required Permission : Just add below line to validate permission : view group permission
    check_user_permission(request,Model_App_Name,'view_group')    
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data     
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # set default page
    page_num = request.page_num
    # default sort order
    sort_order = sorting_order(request,'id')
    # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
    # if url variable not set then achor tag not set except when is_icon set url field is mandatory
    # active is used for not clickable breadcrumbs
    data['breadcrumbs'] = {
            _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
            _('Group') : {'active' : True}
    }
    data['title'] = _('Master - Group')
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('Add Group') : {'url' : '/accounts/group/add' , 'icon' : 'icon-add text-primary'},        
    }

    # Check Post Method is Call or not
    filter_array = {} # default value
    filter_form = {}
    # Handle Post method    
    if request.method == "POST":
        # Filter Button         
        if request.POST.get("filter") and request.POST.get("filter") == 'Filter': 
            search_key = request.POST.get('search','')
            # Check If Search Key not empty
            if search_key:
                # icontains use like %name%
                filter_array['name__icontains'] = search_key   
                filter_form['name'] = search_key
            request.session['group_master_conditions'] = filter_array
            request.session['group_master_form_data'] = filter_form
        # Reset all existing session and form data
        elif request.POST.get('reset') and request.POST.get('reset') == 'Reset':
            request.session['group_master_conditions'] = {}  
            request.session['group_master_form_data'] = {}      
    # Form Persistence : form data send into template
    filter_array = request.session.get('group_master_conditions',{})
    filter_form = request.session.get('group_master_form_data',{})    
    # pass data into template for 
    data['filter_form'] = filter_form
    # create Object of data model
    results_obj = Group.objects.all().filter(**filter_array).order_by(sort_order);
    # find record by number of listing as you required per page
    paginator = Paginator(results_obj,request.pagination_record)
    total_result_count = paginator.count    
    # get result of a particualar page number
    results = paginator.get_page(page_num)  
    # send result to template  
    data['results'] = results    
    # send total count of record in django template
    data['total_result_count'] = total_result_count
    # Page listing count send into template
    data['listing_count'] = request.pagination_record    
    return render(request,'authenticate/view_group.html',data)

# Master function for adding/update Group
@login_required
def add_group(request, id = '0'):
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View Group') : {'url' : '/accounts/group/' , 'icon' : 'icon-add text-primary'},        
    }
    # check whether this is new entries or update existing entries
    if id != '0':
        # Check Required Permission : Just add below line to validate permission : view group permission
        check_user_permission(request,Model_App_Name,'change_group')
        # form persistence
        try:
            data['group_obj'] = Group.objects.get(id = id)
        except:
            data['group_obj'] = False
        # If no data found that means either wrong id pass or
        #  record not found than redirect page to view page
        if not data['group_obj']:
            pnotify(request,'Master : Group','Group id invalid','danger')
            response = redirect('/accounts/group/')
            return response

        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                'Home' : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                'Group' : {'url' : '/accounts/group/'},
                'Edit Group' : {'active' : True}
        }
        data['title'] = _('Master - Edit Group')
    else:
        # Check Required Permission : Just add below line to validate permission : view group permission
        check_user_permission(request,Model_App_Name,'add_group')
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('Group') : {'url' : '/accounts/group/'},
                _('Add Group') : {'active' : True}
        }
        data['title'] = _('Master - Add Language')
    # Handle Post method    
    if request.method == "POST":
        post_data = request.POST
        group = post_data.get('group')
        # In case of new entries
        if id == '0' :
            # Check duplicate language validation
            record_exists = Group.objects.filter(name__iexact = group.strip()).count()
            # No Record Found            
            if record_exists == 0:
                group_obj = Group()
                group_obj.name = group
                group_obj.status = True
                # finally save the object in db                        
                group_obj.save()
                data['pnotify'] = pnotify(request,_('Master : Group'),_('New Group Saved Successfully'),'success')
                return redirect('/accounts/group/')
            else:            
                # Through Error
                data['pnotify'] = pnotify(request,_('Master : Group'),_('Group Already Exists'),'danger')
                data['group_error'] = _('Group Already Exists')
                data['group'] = group
        else:
            # In Case of updation Record
            # Check duplicate language validation
            record_exists = Group.objects.filter(name__iexact = group.strip()).exclude(id = id).count()
            # No Record Found            
            if record_exists == 0:
                group_obj = Group.objects.get(id = id)
                group_obj.name = group
                # Update Record
                group_obj.save()
                data['pnotify'] = pnotify(request,_('Master : Group'),_('Edit Group Saved Successfully'),'success')                
                return redirect('/accounts/group/')
            else:
                # Through Error
                data['pnotify'] = pnotify(request,_('Master : Group'),_('Group Already Exists'),'danger')
                data['group_error'] = _('Group Already Exists')
                data['group'] = group
    return render(request,'authenticate/add_group.html',data)

# Master function for adding/update Group Permission
@login_required
def edit_permission(request, id = '0'):
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View_Group') : {'url' : '/accounts/group/' , 'icon' : 'icon-add text-primary'},        
    }
    # check whether this is new entries or update existing entries
    if id != '0':
        # Check Required Permission : Just add below line to validate permission : view group permission
        check_user_permission(request,Model_App_Name,'change_permission')
        # form persistence
        try:
            data['group_obj'] = Group.objects.get(id = id)
        except:
            data['group_obj'] = False
        # If no data found that means either wrong id pass or
        #  record not found than redirect page to view page
        if not data['group_obj']:
            pnotify(request,'Master : Group','Group id invalid','danger')
            response = redirect('/accounts/group/')
            return response
        elif not data['group_obj'].status:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        # All permission available in System        
        permissions = Permission.objects.all().order_by('group')
        distinct_permission = {}
        # for permission in permissions:
        for permission in permissions:
            # Make as per required value in another dict so we remove duplication
            temp_permission = {permission.id : {
                'app_label' : permission.content_type.app_label,
                'model' : permission.content_type.model,
                'name' : permission.name
                }}
            distinct_permission.update(temp_permission)        
        data['permissions'] = distinct_permission
        # All permission assgined to a given group
        group_permissions = data['group_obj'].permissions.all()
        # Saved All id in group permission id which assigned to given group
        data['group_permission_id'] = [group_permission.id for group_permission in group_permissions]              
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                'Home' : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                'Group' : {'url' : '/accounts/group/'},
                'Edit Group Permission' : {'active' : True}
        }
        data['title'] = _('Master - Edit Group Permission')
    else:
        data['pnotify'] = pnotify(request,'Master : Group Permission','Wrong Url Redirection','success')                
        return redirect('/accounts/group/')   
    # Handle Post method    
    if request.method == "POST":
        post_data = request.POST        
        post_permissions = post_data.getlist('permissions')
        # Make a group model objects
        group_obj = data['group_obj']
        # delete all existing group permission         
        group_obj.permissions.clear()
        for post_permission in post_permissions:
            permission_obj = Permission.objects.get(id = post_permission)
            # Add Permission to a particular Group
            data['group_obj'].permissions.add(permission_obj)
        pnotify(request,'Master : Group Permission','Permission Saved Successfully','success')
        return redirect('/accounts/group/')                               

    return render(request,'authenticate/edit_permission.html',data)

def test(request):
    from django.core import mail
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    # Construct an email message that uses the connection
    email1 = mail.EmailMessage(
        'Hello',
        'Body goes here',
        'yaarloveyou2@gmail.com',
        ['singhnk288@gmail.com'],
        connection=connection,
    )
    email1.send() # Send the email
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'yaarloveyou2@gmail.com',
    #     ['singhnk288@gmail.com'],
    #     fail_silently=False,
    # )
    return HttpResponse("hiii")

@login_required
def change_status(request,master = False, id = False, status = False):    
    if master and id:                                
        # Group master status change from this condition
        if master == 'group':
            # Check Required Permission : Just add below line to validate permission : change group permission
            check_user_permission(request,Model_App_Name,'change_group')
            try:
                group_obj = Group.objects.get(id = id)
            except:
                group_obj = False
            if group_obj:
                group_obj.status = status
                group_obj.save()
                pnotify(request,_('Master_Group'),_('Group_Edit_Successfully'),'success')
            else:
                pnotify(request,_('Master_Group'),_('Group_Not_Edit_Successfully'),'danger')
        # User master status change from this condition
        elif master == 'user':
            # Check Required Permission : Just add below line to validate permission : change user permission
            check_user_permission(request,Model_App_Name,'change_user')
            # Note If User trying to disable own then immediate user logout
            try:
                obj_user = User.objects.get(id = id)
            except:
                obj_user = False
            if obj_user:
                obj_user.is_active = status
                obj_user.save()
                pnotify(request,_('Master_User'),_('User_Edit_Successfully'),'success') 
            else:
                pnotify(request,_('Master_User'),_('User_Not_Edit_Successfully'),'danger')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))