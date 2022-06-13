from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User

from rest_framework import authentication
from rest_framework import exceptions

@login_required(login_url="/accounts/login/")
def redirect_if_not_logged(request):
    html_template = loader.get_template('frontend/index.html')
    context = {'auth':request.user.auth_token}

    return HttpResponse(html_template.render(context, request))