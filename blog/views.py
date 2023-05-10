from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

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


    # def get_context_data(self, **kwargs):
    #     context = super(PostCreateView, self).get_context_data(**kwargs)
    #
    #     context["categories"] = [1, 2, 3]
    #     return context

#
# def blogpost_list(request):
#     all_blogposts = Post.objects.all().order_by('-published_at')
#     post_list = Paginator(all_blogposts, 4)
#     # page = request.GET.get('page')
#     # post_list = paginator.get_page(page)
#
#     return render(request, 'home/index.html', {'post_list': post_list})

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home:index')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
