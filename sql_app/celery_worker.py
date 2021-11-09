import time
from celery import Celery


# Initialize celery
celery = Celery('tasks',
                broker='amqp://guest:guest@127.0.0.1:5672//',
                backend_url='redis://localhost:6379/0')

@celery.task
def create_order(a):
    time.sleep(5)
    return 'canino guardado'
