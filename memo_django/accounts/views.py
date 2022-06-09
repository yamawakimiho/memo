from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader

@login_required(login_url="/accounts/login/")
def redirect_if_not_logged(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('frontend/index.html')
    return HttpResponse(html_template.render(context, request))