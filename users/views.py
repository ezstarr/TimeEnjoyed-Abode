from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Register a new user"""
    # checks whether we are responding to a post request.
    if request.method != 'POST':
        # Display blank registration form
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log user in, redirect to home page
            login(request, new_user)
            return redirect('home:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def logout(request):
    return render(request, 'users/logout.html')


def you(request):
    return render(request, 'users/you.html')

