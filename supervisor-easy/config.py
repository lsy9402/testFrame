from Server import Server

SERVERS = [
    Server(
        name='celery1',
        host='127.0.0.1',
        port=9001,
        user='user',
        password='123'
    )
]

GROUPS = [
    {
        'name': 'celery',
        'apps': ['celery1.gunicorn']
    }
]
