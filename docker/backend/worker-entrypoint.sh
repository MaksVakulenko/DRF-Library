#!/bin/sh

until cd /app/backend
do
    echo "Waiting for Django application (server volume)..."
done

#export PYTHONPATH=/app/backend
# run a worker :)
celery -A DjangoCore worker --loglevel=info --concurrency 1 -E
# The script just start a single worker. You can increase number of workers by changing --concurrency parameter.
