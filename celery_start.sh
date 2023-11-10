celery -A Teachmint beat -l INFO

celery -A Teachmint worker -l info




# celery -A Teachmint.celery worker --pool=solo -l info
# celery -A Teachmint.celery worker  -l info




# $ celery -A Teachmint beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler