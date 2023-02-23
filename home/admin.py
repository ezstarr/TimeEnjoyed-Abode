from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suggestion, ToDoList, Item, Profile, Deck, TarotCard, DeckTarot_Connector



# Register your models here.

# Model viewed through admin
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'date_added', 'author']
    search_fields = ['text', 'date_added', 'author']
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']
    search_fields = ['id', 'username']
    list_per_page = 10


class DeckAdmin(ImportExportModelAdmin):
    list_display = ['id', 'deck_name']
    search_fields = ['id', 'deck_name']
    list_per_page = 10


class TarotCardAdmin(ImportExportModelAdmin):
    list_display = ['deck', 'number']
    resources_class = DeckTarot_Connector
    list_per_page = 20


admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Deck, DeckAdmin)
admin.site.register(TarotCard, TarotCardAdmin)


