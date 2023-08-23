from django.urls import path, re_path
import women.views
from .views import *
from women.views import IndexView, PostFormEditView, PostFormDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # http://127.0.0.1:8000/women/
    # path('post/<slug:post_slug>/edit/', PostFormEditView.as_view(), name='posts_update'),
    # path('post/<slug:post_slug>/delete/', PostFormDeleteView.as_view(), name='posts_delete'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
