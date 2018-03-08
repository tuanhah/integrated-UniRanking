from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import University, UniversitySubject, UniversityScore

def university_info(request,id):
    university = get_object_or_404(University,pk = id)
    subjects = university.subjects.order_by("group")
    return render(request, "university/info.html", {'university' : university, 'subjects' : subjects})
