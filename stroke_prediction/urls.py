"""stroke_prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.first),
    path('index/',views.index),
    path('register/addreg',views.addreg),
    path('register/',views.register),
    path('login/addlogin',views.addlogin),
    path('login/',views.login),
    path('addlogin/',views.addlogin),
    
    path('v_users/',views.v_users, name='v_users'),
    
    path('predict/',views.predict_stroke),
    
    path('prediction_history/',views.prediction_history),
    path('admin_predictions/',views.admin_predictions),
    
    # Consultation Routes
    path('request_consultation/<int:prediction_id>/', views.request_consultation, name='request_consultation'),
    path('admin_consultation_requests/', views.admin_consultations, name='admin_consultation_requests'),
    path('consultation_status/', views.view_consultation_status, name='consultation_status'),
    path('admin_consultations/', views.admin_consultation_requests, name='admin_consultations'),
    path('approve_consultation/<int:consultation_id>/', views.approve_consultation, name='approve_consultation'),
    path('reject_consultation/<int:consultation_id>/', views.reject_consultation, name='reject_consultation'),
    
    # Doctor Routes
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
    path('update_consultation/<int:consultation_id>/', views.update_consultation_response, name='update_consultation'),
    path('admin_doctor_approvals/', views.admin_doctor_approvals, name='admin_doctor_approvals'),
    path('approve_doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('reject_doctor/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    
    # Forgot Password Routes
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('doctor_forgot_password/', views.doctor_forgot_password, name='doctor_forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('reset_doctor_password/<str:token>/', views.reset_doctor_password, name='reset_doctor_password'),
    
    path('logout/',views.logout),
    path('admin/', admin.site.urls),
    path('user_profile', views.user_profile, name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
