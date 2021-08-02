from django.urls import path
from . import views



app_name = 'get_form'

urlpatterns = [
    path('', views.get_form, name='get_form'),
]
