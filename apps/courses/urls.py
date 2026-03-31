from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('create/', views.create_course, name='create_course'),
    path('<slug:slug>/', views.course_detail, name='detail'),
    path('<slug:slug>/learn/', views.course_inner_dashboard, name='inner_dashboard'),
    path('<slug:slug>/edit/', views.edit_course, name='edit_course'),
    path('<slug:slug>/add-lesson/', views.add_lesson, name='add_lesson'),
]
