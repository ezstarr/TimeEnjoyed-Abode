from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
# Create your views here.


def CategoryFuncView(request, categ_name):
    category_posts = Post.objects.filter(categories__name=categ_name)
    return render(request, 'blog/categories.html', {'category_posts': category_posts, 'categ_name':categ_name})


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


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')




