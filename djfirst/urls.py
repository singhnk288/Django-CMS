"""djfirst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')) 
"""
from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/', include('account.urls')),
    path('master/', include('cms_master.urls')),
    path('admin/', admin.site.urls),
    path('datetimes', views.current_datetime, name = "datetimes" ),
    path('', include('cms_master.urls')),
    # Language Translation 
    path('i18n/', include('django.conf.urls.i18n')),
    # favicon ico set
    path('favicon.ico',RedirectView.as_view(url='/static/img/favicon.ico')),    
]

handler404 = 'djfirst.custom_function.not_found'
handler500 = 'djfirst.custom_function.server_error'
handler403 = 'djfirst.custom_function.permission_denied'
handler400 = 'djfirst.custom_function.bad_request'