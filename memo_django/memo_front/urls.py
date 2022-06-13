from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'memo_front'

urlpatterns = [
    path('list/<slug:card_list_id>/', views.card_list, name="card_list"),
    path('<slug:card_id>/', views.assigment, name="assigment")
]