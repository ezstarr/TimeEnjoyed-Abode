from . import views
from django.urls import path


app_name = 'blog'

urlpatterns = [
    # Lists all the blog posts
    path('', views.PostListView.as_view(), name='post-list'),
    # Creates a new post
    path('post/add/', views.PostCreateView.as_view(), name='post-create'),
    # Page of specific post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-details'),
    # Shows prefilled form of specific post.
    path('post/edit/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),



    ]
