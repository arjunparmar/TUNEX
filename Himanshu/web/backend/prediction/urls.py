from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('form/', views.form_view, name='form'),
]
