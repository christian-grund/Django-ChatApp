from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]