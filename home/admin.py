from django.contrib import admin
from .models import Suggestion, ToDoList, Item, Profile



# Register your models here.

# Model viewed through admin
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'date_added', 'owner']
    search_fields = ['text', 'date_added', 'owner']
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']
    search_fields = ['id', 'username']
    list_per_page = 10


admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Profile)

