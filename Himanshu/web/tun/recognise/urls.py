from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name="home"),
    path('form/', views.form, name="form"),
    path('livefeed/', views.livefeed, name="livefeed"),
    path('showlive/', views.showlive, name="showlive"),
    path('liveres/', views.liveres, name="liveres"),
]
