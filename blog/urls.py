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
    # View for Deleting a post
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),

    # Page that shows all the categories
    path('categories/<str:categ_name>/', views.CategoryFuncView, name='categories'),

    # Page that shows only posts of logged-in user:
    path('<str:author_id>/', views.MyPosts, name="my-posts"),
    path('published/<str:author_id>/', views.MyPublished, name="my-published"),
    path('drafts/<str:author_id>/', views.MyDrafts, name="my-drafts"),
    ]
