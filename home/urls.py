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

]
