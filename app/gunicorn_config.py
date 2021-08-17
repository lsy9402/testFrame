import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1

backlog = 2048
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
daemon = False
debug = True
proc_name = 'gunicorn_demo'
pidfile = './log/gunicorn.pid'
errorlog = './log/gunicorn.log'
