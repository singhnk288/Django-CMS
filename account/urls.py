from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Url Dispather : account or account/login redirect to system login page.
    # Url Dispather : account/logout redirect to again login page.
    path('login/', views.user_login, name='Account_Login'),
    path('logout/', views.user_logout, name='Account_Logout'),
    # Add User With Mapping of one or More Group : Group Associated with one or more permission
    path('user/', views.view_user, name='View_User'),
    path('user/add/', views.add_user, name='Add_User'),
    path('user/add/<id>', views.add_user, name='Edit_User'),
    # Add Group 
    path('group/', views.view_group, name='View_Group'),
    path('group/add/', views.add_group, name='Add_Group'),
    path('group/add/<id>', views.add_group, name='Edit_Group'),
    # Group -> Mapped With existing permission
    path('group/permission/<id>', views.edit_permission, name='Edit_Permission'),

    # test
    path('test',views.test,name='test'),

    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('',views.user_login,name ='Login'),
    path('change_status/<master>/<id>/<status>/',views.change_status,name ='Change_Status_Account'), # Change Master status : Enable or Disable    
]
