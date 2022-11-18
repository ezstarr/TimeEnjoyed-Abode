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
    # path('profile/', views.profile_get, name='profile'),
    # path('profile/', views.profile_post, name='profile'),

    # CRUD Pattern for Profile (create, read, update, delete)
    path('profile/<str:user>/', views.profile_view, name='profile-view'),
    # path('profile/<int:id>/update/', views.profile_update, name='profile-update'),

    # Navbar Links
    path('about', views.about, name='about'),
    path('watercolor', views.watercolor, name='watercolor'),

    path('coding', views.coding, name='coding'),
    path('tarot', views.tarot, name='tarot'),
    path('story', views.story, name='story'),

    # User Login
    # path('users/', include('users.urls')),

    # Suggestion feedback pages:
    path('new_suggestion', views.new_suggestion, name='new_suggestion'),
    path('suggestion_review/<int:suggestion_id>/', views.suggestion_review, name='suggestion_review'),

    # To-Do
    path("create/", views.create, name="create"),
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

