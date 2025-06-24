from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('delete/<int:task_id>/', views.delete_task),
    path('edit/<int:task_id>/', views.edit_task),
]
