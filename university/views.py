from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import University, UniversitySubject, UniversityScore
from subject.forms import SubjectForm
from subject.models import GroupSubject

def university_info(request,id):
    university = get_object_or_404(University,pk = id)
    subjects = university.subjects.order_by("group")
    context = {'university' : university}
    editable = True
    if editable: 
        subject_sectors = GroupSubject.objects.filter(parent = None)
        context["subject_sectors"] = subject_sectors
    return render(request, "university/info.html", context)
