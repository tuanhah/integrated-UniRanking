from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
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

def rank(request):
    return render(request, 'rank/rank.html')
def index(request):
	# subject = SubjectGroup.objects.all()
	# context = {'SubjectGroup' : subject}
	return render(request, 'UniRanking/index.html')
def compare(request):
	# GroupSub = SubjectGroup.objects.all()
	# Sub = Subject.objects.all()
	# CateCrit = CategoryCriterion.objects.all()
	# Crit = Criterion.objects.all()
	Uni = University.objects.all()
	context = {'University': Uni}
	return render(request, 'UniRanking/compare.html', context)
def ranking(request):
	# CaCr = CategoryCriterion.objects.all()
	# Uni = University.objects.all()
	# Gs = SubjectGroup.objects.all()
	# sub = Subject.objects.all()
	# usbc = UniversityScoreByCategory.objects.all()
	# context = {'University': Uni, 'SubjectGroup' : Gs, 'CategoryCriterion': CaCr, "UniversityScoreByCategory": usbc, 'Subject': sub}
	return render(request, 'Uniranking/ranking.html')

def info(request):
	# CateCrit = CategoryCriterion.objects.all()
	# Crit = Criterion.objects.all()
	# Uni = University.objects.all()
	# usbc = UniversityScoreByCategory.objects.all()
	# context = {'CategoryCriterion' : CateCrit, 'Criterion' : Crit, 'University' : Uni, 'UniversityScoreByCategory': usbc}
	return render(request, 'UniRanking/university-info.html')
def contact(request):
	return render(request, 'UniRanking/contact.html')
def help(request):
	return render(request, 'UniRanking/help.html')
def register(request):
	return render(request, 'UniRanking/register.html')
def rank(request):
	return render(request, 'UniRanking/rank.html')    
