from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader

@login_required(login_url="/accounts/login/")
def card_list(request, card_list_id):
    html_template = loader.get_template('frontend/cards/index.html')
    context = {'card_list_id': card_list_id}

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/accounts/login/")
def assigment(request, card_id):
    html_template = loader.get_template('frontend/cards/assigment.html')
    context = {'card_id': card_id}

    return HttpResponse(html_template.render(context, request))
