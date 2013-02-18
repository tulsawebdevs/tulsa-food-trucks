from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
# from django.views.decorators.csrf import csrf_exempt
from emailusernames.forms import EmailAuthenticationForm

from .forms import (RegisterForm, VerifyEmailForm, VerifyPhoneForm)

from .models import PhoneVerification, EmailVerification


def login(request):
    return auth_login(
        request, template_name='login.html',
        authentication_form=EmailAuthenticationForm)


def logout(request):
    return auth_logout(request, next_page=reverse('companies'))


def register(request):
    if request.user.is_authenticated():
        return redirect('companies')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        assert request.method == 'GET'
        form = RegisterForm()
    return render_to_response(
        'register.html', RequestContext(request, {'form': form}))


# @csrf_exempt
def register_email(request):
    if 'code' in request.REQUEST:
        form = VerifyEmailForm(request.REQUEST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VerifyEmailForm()
    return render_to_response(
        'register_email.html', RequestContext(request, {'form': form}))


# @csrf_exempt
def register_phone(request):
    if 'code' in request.REQUEST:
        form = VerifyPhoneForm(request.REQUEST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VerifyPhoneForm()
    return render_to_response(
        'register_phone.html', RequestContext(request, {'form': form}))