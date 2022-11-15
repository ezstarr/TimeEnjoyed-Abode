from django.shortcuts import render, redirect
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


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        if request.method == 'POST':
            print(request.POST)

            form = ProfileForm(instance=request.user, data=request.POST)
            if form.is_valid():
                # Save, but not really
                profile_form = form.save(commit=False)
                # Add the user
                profile_form.user = request.user
                # Save for real
                profile_form.save()
                context = {'form': form}
                return redirect('home:create-profile', user, context)
        else:
            form = ProfileForm()
        context = {'form': form}
        return render(request, "home/profile.html", context)
    else:
        return HttpResponseForbidden()



class profile_page(CreateView):
    model = Profile
    fields = [
        "user_mbti",
        "childhood_hobbies"
            ]

    def get_initial(self):
        initial_data = super().get_initial()
        pro_page = Profile.objects.get()
        initial_data["todolist"] = todolist
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todolist = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todolist"] = todolist
        context["title"] = "Create a new item"
        return context


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
    # to a list named 'object_list' be default.
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
        form = CreateNewList(response.POST)  #holds all info from form.
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(response, 'home/create.html', {'form': form})




