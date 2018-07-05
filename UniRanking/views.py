from django.http import HttpResponse

from subject.models import *
from django.shortcuts import render, redirect

def test(request):
    score = SubjectScoreByCriterion.objects.first()
    score.score = 7.4
    score.save()
    return HttpResponse("<body></body>")
def index(request):
	return render(request, 'UniRanking/index.html')
def compare(request):
	return render(request, 'UniRanking/compare.html')
def ranking(request):
	return render(request, 'UniRanking/ranking.html')
def info(request):
	return render(request, 'UniRanking/search-info.html')
def contact(request):
	return render(request, 'UniRanking/contact.html')
def help(request):
	return render(request, 'UniRanking/help.html')
def register(request):
	return render(request, 'UniRanking/register.html')
def rank(request):
	return render(request, 'UniRanking/rank.html') 