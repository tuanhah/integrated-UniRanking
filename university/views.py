from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import University
from subject.models import SubjectGroup

def university_info(request,id):
    university = get_object_or_404(University,pk = id)
    user = request.user
    user_is_editor = False
    if user.is_authenticated: 
        if user.has_perm("university.change_university", university):
            user_is_editor = True
    context = {'university' : university, "user_is_editor" : user_is_editor}
    if user_is_editor:
        subject_sectors = SubjectGroup.objects.filter(sector_id = None)
        context["subject_sectors"] = subject_sectors
    return render(request, "UniRanking/university-info.html", context)
