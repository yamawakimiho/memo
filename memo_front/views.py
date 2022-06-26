from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import  render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from rest_framework.authtoken.models import Token

@login_required(login_url="/accounts/login/")
def redirect_if_not_logged(request):
    html_template = loader.get_template("frontend/index.html")
    context = {"auth": request.user.auth_token}

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/accounts/login/")
def card_list(request, deck_id):
    html_template = loader.get_template("frontend/cards/index.html")
    context = {"deck_id": deck_id, "auth": request.user.auth_token}

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/accounts/login/")
def assigment(request, deck_id):
    html_template = loader.get_template("frontend/cards/assigment.html")
    context = {"deck_id": deck_id, "auth": request.user.auth_token}

    return HttpResponse(html_template.render(context, request))

def register_request(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            Token.objects.create(user=user)
            login(request, user)
            return redirect("index")
        else:
            return render(request=request, template_name="registration/register.html", context={"form":form})
    else:
        form = SignUpForm()
    return render(request=request, template_name="registration/register.html", context={"form":form})