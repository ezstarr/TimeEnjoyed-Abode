from django.contrib import admin
from .models import Post, Category
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'author']
    search_fields = ['title', 'body', 'author']
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category)
