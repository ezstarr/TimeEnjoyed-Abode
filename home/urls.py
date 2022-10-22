from django.contrib import admin
from django.urls import path, include
from . import views

# Django admin header customization
admin.site.site_header = "Dashboard Login"
admin.site.site_title = "Welcome To Your Dashboard"
admin.site.index_title = "Welcome To Your Portal"

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),

    # Navbar Links
    path('about', views.about, name='about'),
    path('watercolor', views.watercolor, name='watercolor'),

    path('coding', views.coding, name='coding'),
    path('tarot', views.tarot, name='tarot'),
    path('story', views.story, name='story'),

    # User Login
    path('users/', include('users.urls')),

    # Suggestion feedback pages:
    path('new_suggestion', views.new_suggestion, name='new_suggestion'),
    path('suggestion_review/<int:suggestion_id>/', views.suggestion_review, name='suggestion_review'),

    # To-Do
    path("create/", views.create, name="create"),
    path("todo/", views.todo, name="todo"),
    path("list/<int:id>", views.todo, name="list"), # we're going to look for an int, and pass it to views.py
    path("item-update", views.item_update, name="item-update"),
    path("todo2", views.ListListView.as_view(), name="todo2"),
    path("shows_list", views.shows_list, name="shows_list"),
    path("list2/<int:list_id>/", views.ItemListView.as_view(), name="list2"),

    # Crud List Add
    path("list2/add/", views.ListCreate.as_view(), name="list-add"),
    # Crud Item Add
    path("list2/<int:list_id>/item/add/", views.ItemCreate.as_view(), name="item-add"),

    # Crud Item Edit
    path("list2/<int:list_id>/item/<int:pk>/", views.ItemUpdate.as_view(), name="item-update"),



]

