from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Suggestion
from .forms import SuggestionForm

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
        # Process completed form
        # request.POST passes a dictionary with all our ids, all our diff attributes..
        form = SuggestionForm(data=request.POST)

        if form.is_valid():
            form.save()

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

            return redirect('home:index')
    else:
        form = SuggestionForm(instance=current_suggestion)
        context = {
            'current_suggestion': current_suggestion,
            'form': form,
            }
        return render(request, 'home/suggestion_review.html', context)
