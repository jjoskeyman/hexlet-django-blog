from django.urls import path
from .views import *
from women.views import IndexView, PostFormEditView, PostFormDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # http://127.0.0.1:8000/women/
    # path('post/<slug:post_slug>/edit/', PostFormEditView.as_view(), name='posts_update'),
    # path('post/<slug:post_slug>/delete/', PostFormDeleteView.as_view(), name='posts_delete'),
    path('about/', About.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
