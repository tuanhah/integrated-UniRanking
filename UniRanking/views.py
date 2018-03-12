from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from criteria.models import CategoryCriterion, Criterion
from subject.models import GroupSubject, Subject
from university.models import University

def register(request):
    if request.user.is_anonymous:
        form = UserRegistrationForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
        return render(request, "registration.html",{"form" : form})
    else:
        return redirect("homepage")
def index(request):
	subject = GroupSubject.objects.all()
	context = {'GroupSubject' : subject}
	return render(request, 'UniRanking/index.html', context)
def compare(request):
	GroupSub = GroupSubject.objects.all()
	Sub = Subject.objects.all()
	CateCrit = CategoryCriterion.objects.all()
	Crit = Criterion.objects.all()
	Uni = University.objects.all()
	context = {'GroupSubject' : GroupSub, 'Subject' : Sub, 'CategoryCriterion' : CateCrit, 'Criterion': Crit, 'University': Uni}
	return render(request, 'UniRanking/compare.html', context)
def ranking(request):
	return render(request, 'Uniranking/ranking.html')

def info(request):
	CateCrit = CategoryCriterion.objects.all()
	Crit = Criterion.objects.all()
	Uni = University.objects.all()
	context = {'CategoryCriterion' : CateCrit, 'Criterion' : Crit, 'University' : Uni}
	return render(request, 'UniRanking/university-info.html', context)
def contact(request):
	return render(request, 'UniRanking/contact.html')
def help(request):
	return render(request, 'UniRanking/help.html')
def register(request):
	return render(request, 'UniRanking/register.html')