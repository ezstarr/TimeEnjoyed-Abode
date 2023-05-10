from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # URL for page with all posts in that category...
        raise NotImplementedError("categories don't have a URL yet")
        # return reverse('')


class Post(models.Model):
    title = models.CharField(max_length=100)
    tldr = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    body = MarkdownxField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property  # This is a decorator that allows us to call this method as an attribute aka "managed attribute"
    def formatted_markdown(self):
        return markdownify(self.body)

    def get_absolute_url(self):
        return reverse('blog:post-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    categories = models.ManyToManyField(Category)
    # likes = models.ManyToManyField(User, related_name="liked_posts", blank=True, null=True)  # related_name prevents reverse accessor clash

    STATUS_CHOICES = [
        ('dra', 'Draft'),
        ('pri', 'Private'),
        ('pub', 'Published'),
            ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def get_categories(self):
        category_query = self.categories.all()
        return "".join(category.name for category in category_query)


    def total_likes(self):
        pass
        # return self.likes.count()

    def __str__(self):
        return f"{self.title} | {self.author} | {self.get_categories()}"

    def get_absolute_url(self):
        return reverse('blog:post-details', args=(str(self.id),))
