from django.http import JsonResponse
from django.contrib.auth import login as auth, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

from UniRanking.forms import UserRegistrationForm



def login(request):
    form = AuthenticationForm(None, request.POST)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            auth(request, form.get_user())
            return JsonResponse({'success' : True})
    errors = form.errors.get_json_data()
    return JsonResponse(errors)

def register(request):
    form = UserRegistrationForm(request.POST)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            auth(request, new_user)

            #SEND MAIL
            email = form.cleaned_data['email']
            subject = 'Thank you for registering to our site'
            message = 'Thank you for registering to our site'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)

            return JsonResponse({'success' : True})
    errors = form.errors.get_json_data()
    return JsonResponse(errors)

