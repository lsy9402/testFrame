FROM python:3.8

ADD requirements.txt .
RUN pip install -r requirements.txt
ENV ENV_FILE .env.docker

WORKDIR /app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b","0.0.0.0:8080", "-w", "4", "main:app"]