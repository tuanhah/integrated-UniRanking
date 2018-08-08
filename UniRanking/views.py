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
def overview(request):
	return render(request, 'user/pages/overview.html')
def personal(request):
	return render(request, 'user/pages/personal-page.html')
def favourite_university(request):
	return render(request, 'user/pages/favourite-university.html')
def manage_university(request):
	return render(request, 'user/pages/manage-university.html')
def manage_sector(request):
	return render(request, 'user/pages/manage-sector.html')

