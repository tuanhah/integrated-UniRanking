from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.user.is_anonymous:
        form = UserRegistrationForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
        return render(request, "registration.html",{"form" : form})
    else:
        return redirect("homepage")