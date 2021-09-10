from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('mplist/', views.mplist, name='mplist'),
    path('posts/', views.posts, name='posts'),
    path('search/', views.search, name='search'),
    path('postofmp/<str:id>', views.MPPostListView.as_view(), name='postofmp'),
    path('images/', views.ImagesView, name='images'),
    path('image_search/', views.ImageSearchResultsView, name='image_search_results'),
    ]

