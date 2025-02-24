from flask import Flask
from celery import Celery
import redis

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0',
        REDIS_URL='redis://localhost:6379/0'  # Adicione esta linha
    )
    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = create_app()
celery = make_celery(app)

# Configuração do Redis
redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])

# Mova a importação das rotas para depois da criação da app
from app import routes