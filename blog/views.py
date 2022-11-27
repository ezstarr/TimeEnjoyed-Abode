from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
from .forms import PostForm
# Create your views here.


def CategoryFuncView(request, name):
    category_posts = Post.objects.filter(categories__name=name)
    return render(request, 'blog/categories.html', {category_posts: 'category_posts'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/blogposts.html'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    #fields = '__all__'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'



