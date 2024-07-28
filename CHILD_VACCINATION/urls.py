"""
URL configuration for CHILD_VACCINATION project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from PRIMARY_HEALTH_CENTER import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homePage,name='homePage'),
    path('contactUs/',views.contactUsPage, name='contactUs'),
    path('aboutUs/',views.aboutUsPage, name='aboutUs'),

    path('adminLoginForm/', views.adminLoginForm, name='adminLoginForm'),
    path('adminRegistrationForm/', views.adminRegistrationForm, name='adminRegistrationForm'),
    path('signupAdmin/', views.admin_registration,name='signupAdmin'),
    path('adminLoginForm/adminPage/',views.admin_page,name='admin_page'),

    
    path('userLoginForm/', views.userLoginForm, name='userLoginForm'),
    path('userRegistrationForm/', views.userRegistrationForm, name='userRegistrationForm'),
    path('signupUser/',views.user_registration,name='signupUser'),
    path('userLoginForm/userPage/',views.user_page,name='user_page'),
    path('user/<str:user_id>/', views.user_detail, name='user_detail'),
    path('delUser/',views.delete_user,name='delUser'),

    path('childRegistrationForm/', views.childRegistrationForm, name='childRegistrationForm'),
    path('signupChild/',views.child_registration,name='signupChild'),
    path('delChild/',views.delete_child,name='delChild'),
    path('updChild/',views.update_child,name='updChild'),
    path('child/<str:child_id>/', views.child_detail, name='child_detail'),

    path('forpwd/',views.forgot_password,name='forpwd'),
    path('emailVerify/',views.verify_email, name='emailVerify'),
    path('forpwdForm/', views.forgetPasswordForm, name='forpwdForm'),
    path('chanpwd/',views.change_password,name='chanpwd'),
    path('vaccDone/',views.vacc_done,name='vaccDone'),
    path('searchVaccDone/',views.search_vacc_done,name='searchVaccDone'),
    path('vaccRemainderMail/',views.vacc_remaind_again,name='vacc_remaind_again'),
    
    
]
