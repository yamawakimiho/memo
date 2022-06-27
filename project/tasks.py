import time
from celery import add_periodic_task
from datetime import timedelta


from django.template.loader import render_to_string
from django.core.mail import EmailMessage

