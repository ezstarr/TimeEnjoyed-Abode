from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blog/blogposts.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = '__all__'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'



