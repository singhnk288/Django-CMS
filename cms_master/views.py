# Import reqired library
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.conf import settings
from cms_master.models import *
from django.shortcuts import redirect
from djfirst.custom_function import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import *
from django.utils.translation import to_locale, get_language

# Define Custom model app name so if any change need you can directly from this global name
Model_App_Name = 'cms_master'

# Master function for view country and also applied filter.
@login_required
def view_country(request):

    # Check Required Permission : Just add below line to validate permission
    check_user_permission(request,Model_App_Name,'view_country')    
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
            _('Country') : {'active' : True}
    }    
    data['title'] = _('Master_Country_Title')
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('Add_Country') : {'url' : '/master/country/add' , 'icon' : 'icon-add text-primary'},        
    }    
    # Check Post Method is Call or not
    filter_array = {} # default value
    filter_form = {}
    
    # Handle Post method
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
                filter_array = {'country__icontains' : search_key}
                filter_form['name'] = search_key.strip()                
            request.session['country_master_conditions'] = filter_array
            request.session['country_master_form_data'] = filter_form
        # Reset all existing session and form data
        elif request.POST.get('reset') and request.POST.get('reset') == 'Reset':
            request.session['country_master_conditions'] = {}  
            request.session['country_master_form_data'] = {}      
    # Form Persistence : form data send into template
    filter_array = request.session.get('country_master_conditions',{})
    filter_form = request.session.get('country_master_form_data',{})  
    filter_array['langauge__code__contains'] = get_language()
    
    # pass data into template for 
    data['filter_form'] = filter_form    
    # create Object of data model
    if filter_array:
        results_obj = CountryMappingLanguage.objects.filter(**filter_array).all().order_by(sort_order)
    else:        
        results_obj = CountryMappingLanguage.objects.all().filter().order_by(sort_order)               
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

    return render(request, 'master/view_country.html', data) 

# Master function for adding/update country
@login_required
def add_country(request,id = '0'):
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View_Country') : {'url' : '/master/country' , 'icon' : 'icon-add text-primary'},        
    }
    # icontains use like %name%
    # user search from user name , first name , last name , email
    # filter_array = get_query(search_key,['username','email','first_name','last_name'])
    filter_language = {'status' : True}
    # Q object is used to create complex query    
    filter_string_language = Q()    
    # Get all language status as true so we add all country with all language
    for item_language in filter_language:
        filter_string_language |= Q(**{item_language:filter_language[item_language]})
    data['language_list'] = Language.objects.all().filter(filter_string_language).order_by('code')    
    # check whether this is new entries or update existing entries
    if id != '0':
        # Check Required Permission : Just add below line to validate permission : change country permission
        check_user_permission(request,Model_App_Name,'change_country')
        # form persistence
        data['country_obj'] = CountryMappingLanguage.objects.filter(country_foriegn_id = id,langauge__status = True).all()        
        data['country_mapping_id'] = id
        if not data['country_obj']:
            response = redirect('/master/country')
            return response        
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('Country') : {'url' : '/master/country'},
                _('Edit_Country') : {'active' : True}
        }
        data['title'] = _('Master_Edit_Country_Title')
    else:
        # Check Required Permission : Just add below line to validate permission : add country permission
        check_user_permission(request,Model_App_Name,'add_country')

        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('Country') : {'url' : '/master/country'},
                _('Add_Country') : {'active' : True}
        }
        data['title'] = _('Master_Add_Country_Title')

    # Handle Post method    
    if request.method == "POST":
        post_data = request.POST
        # dict use for filter purpose
        country_dict = dict()  
        # country list use for saved country this format : list({},{})
        country_list = list()
                                     
        # In case of new entries
        if id == '0' :
            # Check Same name is exist or not            
            # make a dict so we store language_code : Country Name in Country field
            record_exists = 0
            for language in data['language_list']: 
                if language.code and post_data.get('country['+language.code+']'):
                    if not record_exists:  
                        count_record = CountryMappingLanguage.objects.filter(country__icontains = post_data.get('country['+language.code+']').strip()).count()
                        record_exists = count_record
                    country_dict.update({language.code : post_data.get('country['+language.code+']').strip()})                                          
            data['country_dict'] = country_dict 
            # Check duplicate language validation            
            # return HttpResponse(record_exists)
            # No Record Found            
            if record_exists == 0:
                obj_country = Country() 
                obj_country.date_added = datetime 
                # finally save the object in db and retreive country id                                     
                obj_country.save()                             
                if obj_country.id:
                    for language in data['language_list']:
                        obj_mapping_country = CountryMappingLanguage()
                        obj_mapping_country.country_foriegn_id = int(obj_country.id)
                        obj_mapping_country.langauge_id = language.id
                        obj_mapping_country.country = post_data.get('country['+language.code+']').strip()
                        obj_mapping_country.date_added = datetime
                        obj_mapping_country.save()
                else:
                    data['pnotify'] = pnotify(request,_('Master_Country'),_('Country_Not_Saved_Successfully'),'danger')
                
                data['pnotify'] = pnotify(request,_('Master_Country'),_('New_Country_Saved_Successfully'),'success')
                return redirect('/master/country')
            else:            
                # Through Error
                data['pnotify'] = pnotify(request,_('Master_Country'),_('Country_Already_Exists'),'danger')                           
        else:
            # Check Same name is exist or not            
            # make a dict so we store language_code : Country Name in Country field
            record_exists = 0
            for language in data['language_list']: 
                if language.code and post_data.get('country['+language.code+']'):
                    if not record_exists:  
                        count_record = CountryMappingLanguage.objects.filter(country__icontains = post_data.get('country['+language.code+']').strip()).exclude(country_foriegn_id = id).count()
                        record_exists = count_record
                    country_dict.update({language.code : post_data.get('country['+language.code+']').strip()})                                          
            data['country_dict'] = country_dict 
            # In Case of updation Record            
            # No Record Found            
            if record_exists == 0:                 
                CountryMappingLanguage().deleteCountryMappingByForiegnId(id)                                
                for language in data['language_list']:
                    obj_mapping_country = CountryMappingLanguage()
                    obj_mapping_country.country_foriegn_id = int(id)
                    obj_mapping_country.langauge_id = language.id
                    obj_mapping_country.country = post_data.get('country['+language.code+']').strip()
                    obj_mapping_country.date_added = datetime
                    obj_mapping_country.save()  
                data['pnotify'] = pnotify(request,_('Master_Country'),_('Edit_Country_Saved_Successfully'),'success')
                return redirect('/master/country')                
            else:
                # Through Error
                data['pnotify'] = pnotify(request,_('Master_Country'),_('Country_Already_Exists'),'danger')                                

    return render(request,'master/add_country.html',data)

# Master function for view state and also applied relivent filter
@login_required
def view_state(request):
    # Check Required Permission : Just add below line to validate permission : add country permission
    check_user_permission(request,Model_App_Name,'view_state')    
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
            _('State') : {'active' : True}
    }    
    data['title'] = _('Master_Country_Title')
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('Add_State') : {'url' : '/master/state/add' , 'icon' : 'icon-add text-primary'},        
    }    
    # Check Post Method is Call or not
    filter_array_or = {} # default value
    filter_array_and = {} # default value
    filter_form = {}
    # List all country in select2 box
    country_obj = CountryMappingLanguage.objects.all().filter(**{'langauge__code' : get_language(),'country_foriegn__status' : True}).order_by('country')    
    data['country_obj'] = country_obj
    # Handle Post method
    post_country_id = None    
    if request.method == "POST":
        # Filter Button         
        if request.POST.get("filter") and request.POST.get("filter") == 'Filter': 
            search_key = request.POST.get('search','')
            post_country_id = request.POST.get('country_id','')
            # Check If Search Key not empty            
            # icontains use like %name%
            # user search from user name , first name , last name , email                               
            filter_array_or = {'state__icontains' : search_key}
            filter_array_and = {'state_foriegn__country_id' : int(post_country_id),
                                'state_langauge__code__contains' : get_language()}
            filter_form['name'] = search_key.strip()                
            filter_form['country_id'] = int(post_country_id)
            request.session['state_master_conditions_or'] = filter_array_or
            request.session['state_master_conditions_and'] = filter_array_and
            request.session['state_master_form_data'] = filter_form
        # Reset all existing session and form data
        elif request.POST.get('reset') and request.POST.get('reset') == 'Reset':
            request.session['state_master_conditions_or'] = {}  
            request.session['state_master_conditions_and'] = {}
            request.session['state_master_form_data'] = {}      
    # Form Persistence : form data send into template
    filter_array_or = request.session.get('state_master_conditions_or',{})
    filter_array_and = request.session.get('state_master_conditions_and',{})
    filter_form = request.session.get('state_master_form_data',{})
    # filter_array['state_langauge__code__contains'] = get_language()  
    # Q object is used to create complex query    
    or_condition = Q()    
    and_condition = Q()
    
    for item in filter_array_or:
        if filter_array_or[item] and filter_array_or[item] != '':
            or_condition |= Q(**{item:filter_array_or[item]})
    for item in filter_array_and:
        if filter_array_and[item] and filter_array_and[item] != '':
            and_condition &= Q(**{item:filter_array_and[item]})    
    and_condition.add(or_condition, Q.AND) 
    
    # return HttpResponse(and_condition)
    # pass data into template for 
    data['filter_form'] = filter_form
    # return HttpResponse(and_condition)
    # create Object of data model
    if and_condition:
        results_obj = StateMappingLanguage.objects.all().filter(and_condition).order_by(sort_order)
    else:        
        results_obj = StateMappingLanguage.objects.all().filter(state_langauge__code__contains = get_language()).order_by(sort_order)               
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

    return render(request, 'master/view_state.html', data) 

# Master function for adding/update country
@login_required
def add_state(request,id = '0'):    
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View_State') : {'url' : '/master/state' , 'icon' : 'icon-add text-primary'},        
    }
    # icontains use like %name%
    # user search from user name , first name , last name , email
    # filter_array = get_query(search_key,['username','email','first_name','last_name'])
    filter_status = {'status' : True}
    # Q object is used to create complex query    
    filter_string_language = Q()    
    # Get all language status as true so we add all country with all language
    for item_language in filter_status:
        filter_string_language |= Q(**{item_language:filter_status[item_language]})
    data['language_list'] = Language.objects.all().filter(filter_string_language).order_by('code')    

    # List all country in select2 box
    country_obj = CountryMappingLanguage.objects.all().filter(**{'langauge__code' : get_language(),'country_foriegn__status' : True}).order_by('country')    
    data['country_obj'] = country_obj
    # check whether this is new entries or update existing entries
    if id != '0':
        # Check Required Permission : Just add below line to validate permission : add country permission
        check_user_permission(request,Model_App_Name,'change_state')
        # form persistence
        data['state_obj'] = State.objects.filter(id = id).first()
        data['state_mapping_obj'] = StateMappingLanguage.objects.all().filter(state_foriegn_id = id,state_langauge__status = True).order_by('state')
        
        # If no data found that means either wrong id pass or
        #  record not found than redirect page to view page
        if not data['state_obj']:
            response = redirect('/master/state')
            pnotify(request,_('Master_State'),_('State_Id_Invalid'),'danger')
            return response                                      
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('State') : {'url' : '/master/state'},
                _('Edit_State') : {'active' : True}
        }
        data['title'] = _('Master_Edit_State_Title')
    else:
        # Check Required Permission : Just add below line to validate permission : add country permission
        check_user_permission(request,Model_App_Name,'add_state')

        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('State') : {'url' : '/master/state'},
                _('Add State') : {'active' : True}
        }
        data['title'] = _('Master_Add_State_Title')

    # Handle Post method    
    if request.method == "POST":
        post_data = request.POST
        country_id = post_data.get('country_id')       
        # dict use for filter purpose
        state_dict = dict()  
        # country list use for saved country this format : list({},{})
        state_list = list()
        
        data['country_id'] = country_id
        # In case of new entries
        if id == '0' :
            # Check Same name is exist or not            
            # make a dict so we store language_code : State Name in State field
            record_exists = 0
            for language in data['language_list']: 
                if language.code and post_data.get('state['+language.code+']'):
                    # Check duplicate language validation
                    if not record_exists:  
                        count_record = StateMappingLanguage.objects.filter(state__icontains = post_data.get('state['+language.code+']').strip()).count()
                        record_exists = count_record
                    state_dict.update({language.code : post_data.get('state['+language.code+']').strip()})
            data['state_dict'] = state_dict
            # No Record Found            
            if record_exists == 0:
                obj_state = State() 
                obj_state.country_id = country_id
                obj_state.date_added = datetime 
                # finally save the object in db and retreive country id                     
                obj_state.save()                    
                if obj_state.id:
                    for language in data['language_list']:
                        obj_mapping_state = StateMappingLanguage()
                        obj_mapping_state.state_foriegn_id = obj_state.id
                        obj_mapping_state.state_langauge_id = language.id
                        obj_mapping_state.state = post_data.get('state['+language.code+']').strip()
                        obj_mapping_state.date_added = datetime
                        obj_mapping_state.save()
                data['pnotify'] = pnotify(request,_('Master_State'),_('New_State_Saved_Successfully'),'success')
                return redirect('/master/state')
            else:            
                # Through Error
                data['pnotify'] = pnotify(request,_('Master_State'),_('State_Already_Exists'),'danger')                           
        else:
            record_exists = 0
            for language in data['language_list']: 
                if language.code and post_data.get('state['+language.code+']'):
                    # Check duplicate language validation
                    if not record_exists:  
                        count_record = StateMappingLanguage.objects.filter(state__icontains = post_data.get('state['+language.code+']').strip()).exclude(state_foriegn_id = id).count()
                        record_exists = count_record
                    state_dict.update({language.code : post_data.get('state['+language.code+']').strip()})                        
            data['state_dict'] = state_dict
            # In Case of updation Record                        
            # No Record Found            
            if record_exists == 0:
                state_obj = State().getStatebyId(id)
                state_obj.country_id = int(country_id)
                state_obj.save()
                StateMappingLanguage().deleteStateMappingByForiegnId(id)                                
                for language in data['language_list']:
                    obj_mapping_state = StateMappingLanguage()
                    obj_mapping_state.state_foriegn_id = state_obj.id
                    obj_mapping_state.state_langauge_id = language.id
                    obj_mapping_state.state = post_data.get('state['+language.code+']').strip()
                    obj_mapping_state.date_added = datetime
                    obj_mapping_state.save()
                data['pnotify'] = pnotify(request,_('Master_State'),_('Edit_State_Saved_Successfully'),'success')
                return redirect('/master/state')
            else:
                # Through Error
                data['pnotify'] = pnotify(request,_('Master_State'),_('State_Already_Exists'),'danger')                                

    return render(request,'master/add_state.html',data)

# Master function for view language
@login_required
def view_language(request):   
    # Check Required Permission : Just add below line to validate permission : add country permission
    check_user_permission(request,Model_App_Name,'view_language')    
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
            _('Language') : {'active' : True}
    }    
    data['title'] = _('Master_Language_Title')
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('Add_Language') : {'url' : '/master/language/add' , 'icon' : 'icon-add text-primary'},
        # Button 2 As of Now I don' t need another button
        # 'View Language' : {'url' : '/master/language/add' , 'icon' : 'icon-add text-primary'},
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
                filter_array = {'name' : search_key,
                        'code' : search_key,                        
                         }   
                filter_form['name'] = search_key                
            request.session['language_master_conditions'] = filter_array
            request.session['language_master_form_data'] = filter_form
        # Reset all existing session and form data
        elif request.POST.get('reset') and request.POST.get('reset') == 'Reset':
            request.session['language_master_conditions'] = {}  
            request.session['language_master_form_data'] = {}      
    # Form Persistence : form data send into template
    filter_array = request.session.get('language_master_conditions',{})
    filter_form = request.session.get('language_master_form_data',{}) 
    # Q object is used to create complex query    
    filter_string = Q()    
    for item in filter_array:
        filter_string |= Q(**{item:filter_array[item]})   
    # pass data into template for 
    data['filter_form'] = filter_form
    # create Object of data model
    results_obj = Language.objects.all().filter(filter_string).order_by(sort_order);
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
    return render(request,'master/view_language.html',data)

# Master function for adding/update language
@login_required
def add_language(request, id = '0'):
    
    # below line is mandatory to write to set important variable which need in template like APP_NAME 
    data = request.data
    # persistence model app name
    data['model_app_name'] = Model_App_Name
    # Main Page Heading Button
    data['heading_buttons'] = {
        # Format for heading button become standard which present {title => url,icon-class name}
        _('View_Language') : {'url' : '/master/language' , 'icon' : 'icon-add text-primary'},        
    }
    # check whether this is new entries or update existing entries
    if id != '0':
        # Check Required Permission : Just add below line to validate permission : add country permission
        check_user_permission(request,Model_App_Name,'change_langauge')
        # form persistence
        data['language_obj'] = Language().getLanguagebyId(id)
        # If no data found that means either wrong id pass or
        #  record not found than redirect page to view page
        if not data['language_obj']:
            response = redirect('/master/language')
            return response

        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('Language') : {'url' : '/master/language'},
                _('Edit Language') : {'active' : True}
        }
        data['title'] = _('Master_Edit_Language_Title')
    else:
        # Check Required Permission : Just add below line to validate permission : add country permission
        check_user_permission(request,Model_App_Name,'add_langauge')
        # Breadcrumbs Page become dynamic from this section we need heading , url parameter 
        # if url variable not set then achor tag not set except when is_icon set url field is mandatory
        # active is used for not clickable breadcrumbs
        data['breadcrumbs'] = {
                _('Home') : {'url' : settings.HOME_URL,'is_icon' : True,'class' : 'icon-home2 position-left'},
                _('Language') : {'url' : '/master/language'},
                _('Add_Language') : {'active' : True}
        }
        data['title'] = _('Master_Add_Language_Title')
    # Handle Post method    
    if request.method == "POST":
        post_data = request.POST
        language = post_data.get('language')
        language_code = post_data.get('language_code').lower()
        # In case of new entries
        if id == '0' :
            # Check duplicate language validation
            record_exists = Language.objects.filter(name__iexact = language.strip()).count()
            # No Record Found            
            if record_exists == 0:
                obj_lang = Language()
                obj_lang.name = language
                obj_lang.code = language_code
                obj_lang.date_added = datetime                
                # finally save the object in db                        
                obj_lang.save()
                data['pnotify'] = pnotify(request,_('Master_Language'),_('New_Language_Saved_Successfully'),'success')
                return redirect('/master/language')
            else:            
                # Through Error
               data['language_error'] = _('Language_Already_Exists')
               data['language'] = language
               data['language_code'] = language_code
        else:
            # In Case of updation Record
            # Check duplicate language validation
            record_exists = Language.objects.filter(name__iexact = language.strip()).exclude(id = id).count()
            # No Record Found            
            if record_exists == 0:
                obj_lang = Language().getLanguagebyId(id)                                
                obj_lang.name = language
                obj_lang.code = language_code                
                # Update Record
                obj_lang.save()
                data['pnotify'] = pnotify(request,_('Master_Language'),_('Edit_Language_Saved_Successfully'),'success')                
                return redirect('/master/language')
            else:
                # Through Error
               data['language_error'] = _('Language_Already_Exists')
               data['language'] = language
               data['language_code'] = language_code
    return render(request,'master/add_language.html',data)

@login_required
# Ajax function
def change_listing_count(request):
    listing_count = request.GET.get('listing_value', 10)   
    request.session['listing_count'] = listing_count    
    data = {
        'is_status': True
    }
    return JsonResponse(data)

@login_required
def change_status(request,master = False, id = False, status = False):    
    if master and id:
        if master == 'language':
            # Check Required Permission : Just add below line to validate permission : change langauge permission
            check_user_permission(request,Model_App_Name,'change_langauge')
             # Note If User trying to disable own then immediate user logout
            try:
                obj_lang = Language.objects.get(id = id)
            except:
                obj_lang = False
            if obj_lang:
                obj_lang.status = status
                obj_lang.save()
                pnotify(request,_('Master_Language'),_('Language_Edit_Successfully'),'success')
            else:
                pnotify(request,_('Master_Language'),_('Language_Not_Edit_Successfully'),'danger')
        # Country master status change from this condition
        elif master == 'country':
            # Check Required Permission : Just add below line to validate permission : change country permission
            check_user_permission(request,Model_App_Name,'change_country')
            # Note If User trying to disable own then immediate user logout
            try:
                obj_country = Country.objects.get(id = id)
            except:
                obj_country = False
            if obj_country:
                obj_country.status = status
                obj_country.save()
                pnotify(request,_('Master_Country'),_('Country_Edit_Successfully'),'success') 
            else:
                pnotify(request,_('Master_Country'),_('Country_Not_Edit_Successfully'),'danger')  
        # State master status change from this condition                 
        elif master == 'state':
            # Check Required Permission : Just add below line to validate permission : change langauge permission
            check_user_permission(request,Model_App_Name,'change_state')
            # Note If User trying to disable own then immediate user logout
            try:
                obj_state = State.objects.get(id = id)
            except:
                obj_state = False
            if obj_state:
                obj_state.status = status
                obj_state.save()
                pnotify(request,_('Master_State'),_('State_Edit_Successfully'),'success') 
            else:
                pnotify(request,_('Master_State'),_('State_Not_Edit_Successfully'),'danger')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    