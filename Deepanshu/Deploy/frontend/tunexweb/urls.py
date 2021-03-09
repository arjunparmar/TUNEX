from django.urls import path

from .views import tunex_home
from .views import staticpage
from .views import aboutpage
from .views import uploadImage

urlpatterns = [
    path('', tunex_home, name='TUNEX'),
    path('statics/', staticpage),
    path('about/', aboutpage, name='About'),
    path('statics/uploadimage', uploadImage, name='uploadImage'),
]
