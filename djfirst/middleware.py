from django.conf import settings

# This Middleware use to set important variable or important session 
# which we need in view.py file or template file.

class WebInitialization:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.        

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self,request, view_func, *view_args, **view_kwargs):        
        request.data = {            
            'APP_NAME' : settings.APP_NAME,                      
        }        
        # Listing Row is set by ajax session request and we use same function all the time
        request.data['ajax_begining_path'] = '/master/'
        # Set default page number as 1
        request.page_num = request.GET.get('page',1)
        # Set default number of page record 
        request.pagination_record = request.session.get('listing_count', 10)
        # For Pnotify First we check is there any session active for pnotify if yes 
        # then set into request.data and clear notify session else nothing do
        pnotify = request.session.get('pnotify',False)
        
        if pnotify:
            request.data['pnotify'] = pnotify
            request.session['pnotify'] = False
        else:
            request.data['pnotify'] = False
        
        # Return All active Language from System
        request.data['LANGUAGES'] = settings.LANGUAGES

        