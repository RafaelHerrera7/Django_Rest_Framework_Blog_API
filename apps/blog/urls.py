from django.urls import path

from .views import (
    PostListView, 
    PostDetailView,
    PostHeadingsView, 
    IncrementPostClickView,
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug>/headings/', PostHeadingsView.as_view(), name='post-headings'),
    path('posts/increment_click/', IncrementPostClickView.as_view(), name='increment-post-click'),
]