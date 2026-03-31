from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('certificate/<uuid:pk>/', views.verify_certificate, name='verify_certificate'),
]
