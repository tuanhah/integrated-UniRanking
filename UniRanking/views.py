from django.http import HttpResponse

from subject.models import *
from django.shortcuts import render, redirect

def index(request):
	return render(request, 'UniRanking/pages/index.html')
def compare(request):
	return render(request, 'UniRanking/pages/compare.html')
def rank(request):
	return render(request, 'UniRanking/pages/rank.html')
def info(request):
	return render(request, 'UniRanking/pages/search-info.html')
def contact(request):
	return render(request, 'UniRanking/pages/contact.html')
def help(request):
	return render(request, 'UniRanking/pages/help.html')
def personal(request):
	return render(request, 'user/pages/personal.html')
	