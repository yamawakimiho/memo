web: gunicorn project.wsgi
worker: celery -A project worker --events --loglevel info
beat: celery -A project beat
