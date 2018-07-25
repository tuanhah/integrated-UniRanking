from django.http import HttpResponse

from subject.models import *
from django.shortcuts import render, redirect

def index(request):
	return render(request, 'UniRanking/index.html')
def compare(request):
	return render(request, 'UniRanking/compare.html')
def rank(request):
	return render(request, 'UniRanking/rank.html')
def info(request):
	return render(request, 'UniRanking/search-info.html')
def contact(request):
	return render(request, 'UniRanking/contact.html')
def help(request):
	return render(request, 'UniRanking/help.html')