from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    # Home Page
    path('',views.view_country,name ='HOME_PAGE'), # master
    # Country Master
    path('country',views.view_country,name ='View_Country'), # master/country
    path('country/add/',views.add_country,name ='Add_Country'), # master/country/add
    path('country/add/<id>',views.add_country,name ='Edit_Country'), # master/country/add/<id>
    # State Master
    path('state',views.view_state,name ='View_State'), # master/state
    path('state/add/',views.add_state,name ='Add_State'), # master/state/add
    path('state/add/<id>',views.add_state,name ='Edit_State'), # master/state/add
    # City Master    
    path('city',views.view_country,name ='View_City'), # master/state
    path('city/add/',views.add_country,name ='Add_City'), # master/state/add
    path('city/add/<id>',views.add_country,name ='Edit_City'), # master/state/add
    # Language Master
    path('language',views.view_language,name ='View_Language'), # language
    path('language/add/',views.add_language,name ='Add_Language'), # Add language
    path('language/add/<id>',views.add_language,name ='Edit_Language'), # Edit language
    path('change_status/<master>/<id>/<status>/',views.change_status,name ='Change_Status'), # Change Master status : Enable or Disable    

    # Ajax Request : Url Set
    url(r'^ajax/change_listing_count/$', views.change_listing_count, name='Change_Listing_Count'),    
]
