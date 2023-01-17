from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
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

    def get_form(self):
        form = super().get_form()
        list_form = form.save(commit=False)
        list_form.author = self.request.user

        return form


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def get_object(self, queryset=None):
        obj = super(PostUpdateView, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj



class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')

    def get_object(self, queryset=None):
        obj = super(PostDeleteView, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj



