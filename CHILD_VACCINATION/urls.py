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
    path('forpwdForm/', views.forgetPasswordForm, name='forpwdForm'),
    path('userLoginForm/', views.userLoginForm, name='userLoginForm'),
    # path('""/adminLoginForm/', views.admin_login_form),
    path('signupAdmin/',views.admin_registration,name='signupAdmin'),
    # path('loginAdmin/',views.admin_login),
    path('signupUser/',views.user_registration,name='signupUser'),
    path('signupChild/',views.child_registration,name='signupChild'),
    path('forpwd/',views.forgot_password,name='forpwd'),
    path('chanpwd/',views.change_password,name='chanpwd'),
    path('delUser/',views.delete_user,name='delUser'),
    path('delChild/',views.delete_child,name='delChild'),
    path('updChild/',views.update_child,name='updChild'),
    path('celeryTask/',views.celeryTask,name='celeryTask'),
]
