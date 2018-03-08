from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.user.is_anonymous:
        form = UserRegistrationForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
        return render(request, "UniRanking/register.html",{"form" : form})
    else:
        return redirect("homepage")
def index(request): return render(request, 'UniRanking/index.html')
def compare(request): return render(request, 'UniRanking/compare.html')
def info(request): return render(request, 'UniRanking/university-info.html')
def contact(request): return render(request, 'UniRanking/contact.html')
def ranking(request): return render(request, 'UniRanking/ranking.html')
def help(request): return render(request, 'UniRanking/help.hyml')
