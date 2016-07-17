from app import application

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Josh:password@localhost/chain_safe'
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'