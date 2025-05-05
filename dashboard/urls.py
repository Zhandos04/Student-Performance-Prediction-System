from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('support/', views.support, name='support'),
    path('settings/', views.settings, name='settings'),
    path('admin/courses/', views.admin_courses, name='admin_courses'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/run-predictions/', views.run_predictions, name='run_predictions'),
]