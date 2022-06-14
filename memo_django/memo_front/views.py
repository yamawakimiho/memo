from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader

@login_required(login_url="/accounts/login/")
def card_list(request, deck_id):
    html_template = loader.get_template('frontend/cards/index.html')
    context = {'deck_id': deck_id,
    'auth':request.user.auth_token}

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/accounts/login/")
def assigment(request, deck_id):
    html_template = loader.get_template('frontend/cards/assigment.html')
    context = {'deck_id': deck_id,
    'auth':request.user.auth_token}

    return HttpResponse(html_template.render(context, request))
