web: gunicorn project.wsgi
worker: celery -A project worker --events --loglevel info -B
