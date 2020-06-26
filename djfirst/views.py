from django.http import HttpResponse
import datetime
from django.conf import settings
from django.shortcuts import render

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    
def templatehtml(request):
    # app_name and function name are the variable which we use always to pass data into template
    # because this variable used in layout and sidebar
    data = {
        'app_name' : '',
        'function' : 'templatehtml',
        'APP_NAME' : settings.APP_NAME,
    }
    return render(request, 'master/index.html',data)