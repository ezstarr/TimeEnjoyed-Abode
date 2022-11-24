from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'author']
    search_fields = ['title', 'body', 'author']
    list_per_page = 10


admin.site.register(Post)
