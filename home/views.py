from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Suggestion, ToDoList, Item, Profile
from .forms import SuggestionForm, ProfileForm
from django.contrib import messages
from .forms import CreateNewList
from django.http import HttpResponseForbidden


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


# Display Empty Profile Form
def profile(request):
    # if user is logged in:
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    else:
        # if user filled out form -> profile_form
        if request.method == 'POST':
            print(request.POST)

            form = ProfileForm(instance=request.user, data=request.POST)
            if form.is_valid():

                # clean the data
                f_1 = form.cleaned_data["user_mbti"]
                f_2 = form.cleaned_data["childhood_hobbies"]
                profile_form = Profile(user_mbti=f_1, childhood_hobbies=f_2)
                # add user to form
                profile_form.user = request.user
                # Save for real
                profile_form.save()

                profile_form_username = profile_form.user.username
                print(profile_form_username)
                return redirect('home:profile-view', profile_form_username)
        else:
            form = ProfileForm()
            context = {'form': form}
            return render(request, "home/profile.html", context)



# After updating Profile, redirects to profile_read
def profile_view(request, profile_form_username):
    """dict for initial data with
    field name as keys"""
    context = {}
    # "user__username" look for a profile that is linked to user that has the username you want
    context["data"] = Profile.objects.get(user__username=profile_form_username)

    # add the dictionary during initialization
    return render(request, "home/profile_view.html", context)



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
    template_name = "home/todo.html"


class ItemListView(ListView):
    model = Item
    template_name = "home/todo_list.html"

    def get_queryset(self):
        return Item.objects.filter(todolist_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["shows_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    # Gets instantiated as a view via the template
    model = ToDoList
    fields = ["name"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["name"] = "Add a new list"
        return context


class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("home:todo")


class ItemCreate(CreateView):
    # base class for any view designed to create objects
    model = Item
    fields = [
        "todolist",
        "created_date",
        "text",
    ]

    def get_initial(self):
        initial_data = super().get_initial()
        todolist = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todolist"] = todolist
        return initial_data

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
        "created_date",
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
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(response, 'home/create.html', {'form': form})
