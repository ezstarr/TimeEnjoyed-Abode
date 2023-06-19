from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth.decorators import login_required
# Create your views here.


def CategoryFuncView(request, categ_name):
    category_posts = Post.objects.filter(categories__name=categ_name)
    return render(request, 'blog/categories.html', {'category_posts': category_posts, 'categ_name': categ_name})


def MyPosts(request, author_id):
    my_posts = Post.objects.filter(author__id=author_id)
    return render(request, 'blog/my_blogs.html', {'my_posts': my_posts, 'author_id': author_id})

def MyPublished(request, author_id):
    my_published = Post.objects.filter(author__id=author_id, status='pub')
    print(my_published)
    return render(request, 'blog/my_published.html', {'my_published': my_published, 'author_id': author_id})

def MyDrafts(request, author_id):
    my_drafts = Post.objects.filter(author__id=author_id, status='dra')
    return render(request, 'blog/my_drafts.html', {'my_drafts': my_drafts, 'author_id': author_id})


class PostListView(ListView):
    template_name = 'home/index.html'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'




class PostUpdateView(UserPassesTestMixin, UpdateView):
    """UserPassesTestMixin is django's authentication system"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def get_success_url(self):
        print("DOES THIS HIT")
        return reverse_lazy('blog:post-details', kwargs={'pk': self.object.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # Check if the form is valid
    #     if form.is_valid():
    #         print("hi")
    #         # Print any validation errors to the console
    #         print(form.errors)
    #     else:
    #         print("bye")
    #         # If the form is not valid, return a bad request response with the errors
    #         return HttpResponseBadRequest(form.errors)
    #     return response


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home:index')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
