from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Suggestion, ToDoList, Item, Profile, ReadRequest, Card
from .forms import SuggestionForm, ProfileForm, ReadRequestForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import CreateNewList
from django.http import HttpResponseForbidden
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from random import sample, seed
import os

from dotenv import load_dotenv
import datetime

load_dotenv()
# Create your views here.

def index(request):
    return render(request, "home/index.html")


def about(request):
    return render(request, "home/about.html")


def watercolor(request):
    return render(request, "home/watercolor.html")


def coding(request):
    return render(request, "home/coding.html")


# def tarot(request):
#     return render(request, "home/tarot.html")


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


def profile_view(request):
    # # if there is user.profile data...display it
    # ProfileForm(instance=request.user.profile)
    # context = {}
    # # "user__username" look for a profile that is linked to user that has the username you want
    # context["data"] = Profile.objects.get(user__username=profile_form_username)
    # print(request.method)
    # return render(request, "home/profile_view.html", context)
    pass


def profile_update(request, id):
    # context = {}
    #
    # # fetch object related to passed id
    # obj = get_object_or_404(Profile, user=id)
    #
    # # pass the object as instance in form
    # form = ProfileForm(request.POST or None, instance= obj)
    #
    # # save the data from the form and
    # # redirect to profile_view
    # if form.is_valid():
    #     form.save()
    #     return redirect('home:profile-view', request.user.id)
    # context["form"] = form
    # return render(request, "home/profile_update.html", context)
    pass


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
    """ Reading request made through index.html """
    all_cards = Card.objects.all()

    #alternative: Entry.objects.values_list('id', flat=True).order_by('id')
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            int_num = int(request.POST['num'])
            num = max(1, min(int_num, 6))

            question = request.POST['question']
            seed(f"{user}{question}")
            random_cards = sample(list(all_cards), num)

            # create an instance of the model
            request_obj = ReadRequest(user=user)
            request_obj.question = question
            request_obj.num = num
            request_obj.save()

            # manytomanyrel fields need to be added into.
            request_obj.card_ids.add(*random_cards)

            print(request_obj.card_ids.all())

            # Gathers all the objects together
            all_reads = ReadRequest.objects.all().order_by('-date_time')
            new_latest_read = all_reads.latest('date_time')
            form = ReadRequestForm(instance=new_latest_read)
            context = {
                'new_latest_read': new_latest_read,
                'all_reads': all_reads,
                'form': form}

            # User redirected to result & form to rate it.
            # return redirect('home:tarot-rate', latest_data.pk)
            return render(request, 'home/tarot.html', context)
        else:
            user = request.POST['name']
            num = request.POST['num']
            random_cards = sample(list(all_cards), int(num))
            context = {'user': user, 'random_cards': random_cards}

            return render(request, 'home/index.html', context)




def read_result(request, read=None):
    """Linked from navigation bar.
    urls:  tarot-rate, tarot-list"""

    print(read)
    if read is None:
        """LIST - name:tarot-list (read=0), from nav-bar"""
        if request.method == 'GET':
            all_reads = ReadRequest.objects.all().order_by('-date_time')

            # read_request_id = "0"
            context = {
                'all_reads': all_reads,
                # 'read_request_id': read_request_id,
            }
            return render(request, 'home/tarot.html', context)
        if request.method == 'POST':
            all_reads = ReadRequest.objects.all().order_by('-date_time')
            new_latest_read = all_reads.latest('date_time')
            new_latest_read.question = request.POST['question']
            new_latest_read.save()
            form = ReadRequestForm(instance=new_latest_read)
            context = {
                'new_latest_read': new_latest_read,
                'all_reads': all_reads,
                'form': form}

            print("lala")
            return render(request, 'home/tarot.html', context)



    elif read is not None:
        print(f"read = {read}")

        a_read = ReadRequest.objects.get(id=read)
        """UPDATE - name:tarot-rate (read.pk) Edit a tarot read"""
        if request.method == 'POST':
            update = True
            a_read.question = request.POST['question']
            a_read.rating = request.POST['rating']
            a_read.save()
            update_form = ReadRequestForm(instance=a_read)
            context = {
                'update': update,
                'a_read': a_read,
                'update_form': update_form,
                'read': (read,),
            }
            return render(request, 'home/tarot.html', context)
        elif request.method == 'GET':
            get_read_form = True
            print(request.method)
            update_form = ReadRequestForm(instance=a_read)

            # all_reads = ReadRequest.objects.all().order_by('-date_time')

            # context = {'all_reads': all_reads,
            context = {'update_form': update_form,
                       'get_read_form': get_read_form,
                       'a_read': a_read}
            print("does this go through")
            return render(request, 'home/tarot.html', context)


        # This gets added to handle the case is not None and request method is not POST
        else:
            return HttpResponse("Invalid request method.")

def read_result_del(request, read):
    a_read = ReadRequest.objects.get(id=read)
    a_read.delete()
    all_reads = ReadRequest.objects.all().order_by('-date_time')

    return render(request, 'home/tarot.html', {'all_reads': all_reads})


@csrf_exempt
@require_http_methods(["POST"])
def twitch_reads(request):
    if request.POST.get("TWITCHIO_TOKEN") and request.POST.get("TWITCHIO_TOKEN") == os.getenv("TWITCHIO_BOT_TOKEN"):
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


