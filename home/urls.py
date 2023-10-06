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

    # stats
    path('stats_mbti', views.stats_mbti, name='stats-mbti'),
    path('json_mbti_count', views.json_mbti_count, name='json-mbti-count'),

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
    path('tarot/twitch_reads', views.twitch_reads, name='twitch-reads'),

    # instance can get added to user's existing db
    path('tarot/all_reads', views.tarot_list, name='tarot-list'), # GET List
    path('tarot/read_request/', views.read_request, name='read-request'),  # POST new read with id
    path('tarot/detail/<int:read_id>', views.tarot_detail, name='tarot-detail'),  #TODO: understand this line
    path('json_read_result/', views.json_read_result, name='json-read-result'),
    path('tarot/delete/<int:read>', views.read_result_del, name='tarot-delete'),


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
