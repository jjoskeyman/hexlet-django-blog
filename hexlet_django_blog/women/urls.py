from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='main_page'),
    path('articles/', articles, name='articles'),
    path('categories/', categories),
    path('about/', about, name='about'),
    re_path(r'^archive/(?P<year>[0-9]{4})', archive),
]
