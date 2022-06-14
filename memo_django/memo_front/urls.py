from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'memo_front'

urlpatterns = [
    path('list/<slug:deck_id>/', views.card_list, name="card_list"),
    path('assigment/<slug:deck_id>/', views.assigment, name="assigment")
]