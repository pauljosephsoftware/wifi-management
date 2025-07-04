# urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import subscribe_to_plan, subscribe_success

app_name = 'subscription'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('plans/', views.plans, name='plans'),
    path('register/', views.register, name='register'),
    path('view_profile/', views.profile_view, name='view-profile'),
    path('profile/', views.manage_profile, name='manage_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='subscription/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('subscribe/<int:plan_id>/', subscribe_success, name='subscribe_to_plan'),
    path('networks/', views.available_networks, name='available_networks'),
]
