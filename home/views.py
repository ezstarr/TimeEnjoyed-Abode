from django.shortcuts import render, redirect, reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Suggestion, ToDoList, Item
from .forms import SuggestionForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateNewList


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



def todo(response):
    # Show A To-Do List
    t_ls = ToDoList.objects.all()
    t_items = Item.objects.all()
    #ls = ToDoList.objects.get(id=id)
    context = {
        't_ls': t_ls,
        't_items': t_items,
        #'name': ls.name,
        }
    return render(response, 'home/todo.html', context)


def item_update(response):
    pass


def shows_list(response):
    pass


class ListListView(ListView):
    # This page displays the list of To-Do Titles
    # fetches all the ToDoList records from db,
    # turns them into python objs, and appends them
    # to a list named 'object_list' be default.
    model = ToDoList
    template_name = "home/todo2.html"


class ItemListView(ListView):
    model = Item
    template_name = "home/shows_list.html"


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

    # def get_success_url(self):
    #     return reverse("list2", args=[self.object.todo_list_id])


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




