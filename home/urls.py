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


    #profile URL
    path('profile/', views.profile_get_method, name='profile'),

    # Navbar Links
    path('about', views.about, name='about'),
    path('watercolor', views.watercolor, name='watercolor'),
    path('coding', views.coding, name='coding'),
    path('story', views.story, name='story'),

    # User Login
    # path('users/', include('users.urls')),

    # Suggestion feedback pages:
    path('new_suggestion', views.new_suggestion, name='new_suggestion'),
    # path('suggestion_list/', views.SuggestionView.as_view(), name='view_suggestions'),
    path('suggestion_review/<int:suggestion_id>/', views.suggestion_review, name='suggestion_review'),

    # Tarot CRUD:
    path('tarot/twitch_reads', views.twitch_reads, name='twitch-reads'),  # instance can get added to user's existing db
    path('tarot', views.read_request, name='tarot'),  # instantiates, displays, and lists.
    path('tarot/', views.tarot_list, name='tarot_list'),
    path('tarot/<int:read>/', views.read_result, name='tarot-rate'),  # update
    path('tarot/all_my_reads/', views.read_result, name='my_tarot_list'),  # navbar list
    path('tarot/<int:read>/delete', views.read_result_del, name='tarot-delete'),

    path('my-json-endpoint/', views.read_request, name='my-json-endpoint'),
    # path('my-json-endpoint/', views.read_request, name='my-json-endpoint')

    # To-Do
    path("todo", views.ListListView.as_view(), name="todo"),
    path("list2/<int:list_id>/", views.ItemListView.as_view(), name="list2"),

    # CRUD patterns for ToDoList
    path("list2/add/", views.ListCreate.as_view(), name="list-add"),
    path("list2/<int:pk>/delete", views.ListDelete.as_view(), name="list-delete"),

    # CRUD patterns for Items
    path("list2/<int:list_id>/item/add/", views.ItemCreate.as_view(), name="item-add"),
    path("list2/<int:list_id>/item/<int:pk>/", views.ItemUpdate.as_view(), name="item-update"),
    path("list2/<int:list_id>/item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item-delete")

]
