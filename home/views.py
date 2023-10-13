import datetime
import json
import os
from random import sample, seed

import twitch
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from dotenv import load_dotenv

from .forms import SuggestionForm, ProfileForm, ReadRequestForm
from .models import Suggestion, ToDoList, Item, Profile, ReadRequest, Card
from django.db.models import Count

load_dotenv()



def index(request):
    client = twitch.TwitchHelix(
        client_id=os.getenv('DJANGO_CLIENT_ID'),
        client_secret=os.getenv('DJANGO_CLIENT_SECRET'))
    client.get_oauth()

    # list_of_users = User.objects.values()[0]
    # list_of_usernames = list_of_users.get('username')

    # print(client.get_streams(user_logins=['timeenjoyed']))
    # user_ids =
    if client.get_streams(user_ids=['410885037']):
        status = "online"
    else:
        status = "offline"
    blog_queryset = Post.objects.all().order_by('-published_at')
    paginator = Paginator(blog_queryset, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'status': status,
               'page_obj': page_obj}
    return render(request, 'home/index.html', context)


def about(request):
    return render(request, "home/about.html")


def watercolor(request):
    return render(request, "home/watercolor.html")


def coding(request):
    return render(request, "home/coding.html")


def story(request):
    return render(request, "home/story.html")


def profile_get_method(request):
    if request.method == 'GET':
        return profile_get(request)
    # user is saving profile form
    if request.method == 'POST':
        return profile_post(request)
    return HttpResponse(status=405)


def profile_get(request):
    print("profile_get runs")
    Profile.objects.get_or_create(user=request.user)
    print("profile_get_or_create runs")
    form = ProfileForm()
    if request.user.profile:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'home/profile.html', context)


def profile_post(request):
    print("profile_post runs")
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        context = {'profile': profile}
        return render(request, 'home/profile.html', context)
    else:
        print(form.errors)
        return HttpResponse(status=400)

def stats_mbti(request):
    data = Profile.objects.values('user_mbti').annotate(count=Count('user_mbti'))
    context = {'data': data}
    return render(request, 'home/stats_mbti.html', context)

def json_mbti_count(request):
    data = Profile.objects.values('user_mbti').annotate(count=Count('user_mbti'))
    # JSON endpoint
    return JsonResponse(list(data), safe=False)


def stats_zodiac(request):
    data = Profile.objects.values('user_zodiac').annotate(count=Count('user_zodiac'))
    context = {'data': data}
    return render(request, 'home/stats_zodiac.html', context)

def json_zodiac_count(request):
    data = Profile.objects.values('user_zodiac').annotate(count=Count('user_zodiac'))
    # JSON endpoint
    return JsonResponse(list(data), safe=False)

def new_suggestion(request):
    """Gets suggestions"""
    # checks whether we are responding to a post request.
    if request.method == 'POST':
        form = SuggestionForm(data=request.POST or None)

        if form.is_valid():
            suggestion_form = form.save(commit=False)

            suggestion_form.author = request.user
            form.save()
            # TODO: decide which page to put the message alert "Submission Successful"
            return redirect('home:suggestion_review', suggestion_id=form.instance.id)

    else:
        # Display blank suggestion form
        form = SuggestionForm()

    context = {'form': form}
    return render(request, 'home/new_suggestion.html', context)


def suggestion_review(request, suggestion_id):
    current_suggestion = Suggestion.objects.get(id=suggestion_id)
    if request.method == 'POST':
        form = SuggestionForm(instance=current_suggestion, data=request.POST)
        if form.is_valid():
            current_suggestion.user = request.user
            form.save()
            messages.success(request, "Suggestion Submitted!")

            return redirect('home:index')
        else:
            messages.warning(request, "Please fix")
    else:
        form = SuggestionForm(instance=current_suggestion)
        context = {
            'current_suggestion': current_suggestion,
            'form': form,
        }
        return render(request, 'home/suggestion_review.html', context)


class ListListView(ListView):
    # This page displays the list of To-Do Titles
    # fetches all the ToDoList records from db,
    # turns them into python objs, and appends them
    # to a list named 'object_list' by default.
    model = ToDoList
    print("ListList View views.py")
    template_name = "home/todo.html"


class ItemListView(ListView):
    model = Item
    template_name = "home/todo_list.html"

    def get_queryset(self):
        # Filters items of a list of different attributes
        # items_all = Item.objects.filter(todolist_id=self.kwargs["list_id"])
        # items_incomplete = Item.objects.filter(todolist_id=self.kwargs["list_id"], complete=False)
        # context = {
        #     'items_all': items_all,
        #     'items_incomplete': items_incomplete}
        return Item.objects.filter(todolist_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        # Specifies which list of items I want to display
        context = super().get_context_data()
        context["shows_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["items_incomplete"] = Item.objects.filter(todolist_id=self.kwargs["list_id"], complete=False)
        context["items_complete"] = Item.objects.filter(todolist_id=self.kwargs["list_id"], complete=True)
        return context


class ListCreate(CreateView):
    # Gets instantiated as a view via the template
    model = ToDoList
    fields = ['text', 'priority']
    print("ListCreate test")

    # Use for when adding DateTimePickerInput:
    # This overrides Django's default get_form function.
    # Request info is built into it, so no need to pass.
    def get_form(self):
        form = super().get_form()
        # form.fields['deadline'].widget = DateTimePickerInput()
        list_form = form.save(commit=False)
        list_form.author = self.request.user
        # list_form.save()
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(ListCreate, self).get_context_data(*args, **kwargs)
        context["text"] = "Add a new list"
        return context


class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("home:todo")

    # TODO: Make better 403 page
    def get_object(self, queryset=None):
        obj = super(ListDelete, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj


class ItemCreate(CreateView):
    # base class for any view designed to create objects
    model = Item
    fields = [
        "todolist",
        "date_created",
        "text",
        "complete",
    ]

    def get_initial(self):
        initial_data = super().get_initial()
        todolist = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todolist"] = todolist
        return initial_data

    # This sets the author and todolist_id to each item.
    def get_form(self):
        form = super().get_form()
        # form.fields['deadline'].widget = DateTimePickerInput()
        list_form = form.save(commit=False)
        list_form.author = self.request.user
        list_form.todolist = ToDoList.objects.get(id=self.kwargs["list_id"])
        # list_form.save()

        return form

    def get_context_data(self):
        context = super().get_context_data()
        todolist = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todolist"] = todolist
        context["title"] = "Create a new item"
        return context

    # def get_success_url(self):
    #     return reverse("list2", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    # Same as CreateView, except it pre-populate template form with data from existing entries
    model = Item
    fields = [
        "todolist",
        "date_created",
        "text",
        "complete"
    ]

    def get_object(self, queryset=None):
        obj = super(ItemUpdate, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todolist"] = self.object.todolist
        context["text"] = "Edit item"
        return context


class ItemDelete(DeleteView):
    model = Item

    def get_object(self, queryset=None):
        obj = super(ItemDelete, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse("home:list2", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todolist"] = self.object.todolist
        return context


def read_request(request):
    """ Reading request made through base.html <form> """
    all_cards = Card.objects.all()

    # alternative: Entry.objects.values_list('id', flat=True).order_by('id')
    if request.method == 'POST':
        if request.user:
            user = request.user
            is_auth = True
            int_num = int(request.POST['num'])
            num = max(1, min(int_num, 6))
            date_time = datetime.datetime.now()

            question = request.POST['question']
            seed(f"{user}{question}{date_time}")
            random_cards = sample(list(all_cards), num)
            print(random_cards)

            # create an instance of the model
            request_obj = ReadRequest(user=user)
            request_obj.question = question
            request_obj.num = num
            request_obj.save()
            print(request_obj.id)
            request_obj.card_ids.add(*random_cards)
            return redirect('home:tarot-detail', read_id=request_obj.id)  # URL that passes object to a view
        else:
            return HttpResponse(400)

    if request.method == 'GET':
        return HttpResponse(400)

    #     # manytomanyrel fields need to be added into.
    #     request_obj.card_ids.add(*random_cards)
    #
    #     print(request_obj.card_ids.all())
    #
    #     # Gathers all the objects together
    #     all_reads_obj = ReadRequest.objects.all().order_by('-date_time')
    #     new_latest_read = all_reads_obj.latest('date_time')
    #     form = ReadRequestForm(instance=new_latest_read)
    #
    #     context = {
    #         'new_latest_read': new_latest_read,
    #         'all_reads': all_reads_obj,
    #         'is_auth': is_auth,
    #         'request_obj': request_obj,
    #         'form': form}
    #
    # # User redirected to result & form to rate it.
    # return redirect('home:tarot-rate', new_latest_read.pk)
    # # return redirect('home:tarot-rate', read=id)
    # else:
    # user = request.POST['name']
    # num = request.POST['num']
    # random_cards = sample(list(all_cards), int(num))

    # else:
    #     all_reads = ReadRequest.objects.all().order_by('-date_time')
    #     paginator = Paginator(all_reads, 8)
    #     page = request.GET.get('page')
    #     reads = paginator.get_page(page)
    #
    #     return render(request, 'home/tarot.html', {'reads': reads})

    # return render(request, 'home/index.html', context)

def tarot_detail(request, read_id):
    # This get request is made via the client.
    # This function always will receive a read_id from read_request view function.
    if request.method == 'GET':
        specific_read = ReadRequest.objects.get(id=read_id)
        context = {
            'specific_read': specific_read
        }
        return render(request, 'home/tarot_detail.html', context)


def json_read_result(request):
    all_cards = Card.objects.all()
    is_auth = False
    body = json.loads(request.body)
    num = body["num"]
    cards_list = [card.to_dict() for card in all_cards]
    random_cards = sample(list(cards_list), int(num))
    return JsonResponse({"random_cards": random_cards, 'is_auth': is_auth})


def tarot_list(request):
    """GETs list of every tarot read from the NavBar, no ID required"""
    all_reads = ReadRequest.objects.all().order_by('-date_time')
    paginator = Paginator(all_reads, 8)
    page = request.GET.get('page')
    reads = paginator.get_page(page)
    return render(request, 'home/tarot_list.html', {'reads': reads, 'all_reads': all_reads})



@login_required()  # Ensures user is logged in
def read_result_del(request, read):
    a_read = ReadRequest.objects.get(id=read)
    # Check if the logged-in user is the owner of the object
    if request.user == a_read.user:
        a_read.delete()
    return redirect('home:tarot-list')


@csrf_exempt
@require_http_methods(["POST"])
def twitch_reads(request):
    # checks two things, t_token 1) not none 2) matches django
    if request.POST.get("t_token") and request.POST.get("t_token") == os.getenv("T_TOKEN"):
        user_twitch = request.POST['user']
        rating = request.POST['rating']
        user = User.objects.filter(username=user_twitch)

        if user.exists():
            request_obj = ReadRequest(
                rating=rating,
                user=user.first())
            request_obj.save()
            return HttpResponse("Save successful.", content_type="text/plain")

        return HttpResponse("Check if you're logged in.", content_type="text/plain")
    return HttpResponse("Unauthorized")

# @csrf_exempt
# @require_http_methods(["POST"])
# def twitch_saves(request):
#     if request.POST.get("t_token") and request.POST.get("t_token") == os.getenv("T_TOKEN"):
#         if
