from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Suggestion, ToDoList, Item, Profile
from .forms import SuggestionForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CreateNewList
from django.http import HttpResponseForbidden
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

# Create your views here.

def index(request):
    return render(request, "home/index.html")


def about(request):
    return render(request, "home/about.html")


def watercolor(request):
    return render(request, "home/watercolor.html")


def coding(request):
    return render(request, "home/coding.html")


def tarot(request):
    return render(request, "home/tarot.html")


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
        # if request.POST.get("submit"):
        #     # Process completed form
        #     # request.POST passes a dictionary with all our ids, all our diff attributes..
        #     messages.success(request, "Submitted Successfully!")
        #     return redirect('home:suggestion_review')
        # else:
        form = SuggestionForm(data=request.POST or None)

        if form.is_valid():
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
        return Item.objects.filter(todolist_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["shows_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    # Gets instantiated as a view via the template
    model = ToDoList
    fields = ['text', 'priority']

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


class ItemCreate(CreateView):
    # base class for any view designed to create objects
    model = Item
    fields = [
        "todolist",
        "date_created",
        "text",
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

    def get_context_data(self):
        context = super().get_context_data()
        context["todolist"] = self.object.todolist
        context["text"] = "Edit item"
        return context


class ItemDelete(DeleteView):
    model = Item

    def get_success_url(self):
        return reverse("home:list2", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todolist"] = self.object.todolist
        return context


def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)  # holds all info from form.
        if form.is_valid():
            # get name from form
            n = form.cleaned_data["text"]
            t = ToDoList(text=n)
            t.save()
    else:
        form = CreateNewList()
    return render(response, 'home/create.html', {'form': form})
