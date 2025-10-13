from django.urls import path
from . import views

app_name = 'lingua_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/<int:lesson_id>/', views.lesson_view, name='lesson'),
    path('settings/', views.settings_view, name='settings'),
    path('reset-progress/', views.reset_progress, name='reset_progress'),
]