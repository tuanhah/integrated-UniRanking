from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from criteria.models import CategoryCriterion, Criterion
from university.models import University
from subject.models import GroupSubject
def register(request):
    if request.user.is_anonymous:
        form = UserRegistrationForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
        return render(request, "registration.html",{"form" : form})
    else:
        return redirect("homepage")
def index(request): return render(request, 'UniRanking/index.html')
def compare(request): 
	Data = {'University': University.objects.all(), 'GroupSubject': GroupSubject.objects.all(), 'CategoryCriterion':CategoryCriterion.objects.all(), 'Criterion':Criterion.objects.all(),}
	return render(request, 'UniRanking/compare.html', Data)
def info(request):
	Data = {'CategoryCriterion':CategoryCriterion.objects.all(), 'Criterion':Criterion.objects.all(), 'University':University.objects.all(),}

	return render(request, 'UniRanking/university-info.html', Data)
def contact(request): return render(request, 'UniRanking/contact.html')
def ranking(request):
	Data = {'University': University.objects.all(),}
	return render(request, 'UniRanking/ranking.html', Data)
def help(request): return render(request, 'UniRanking/help.html')
