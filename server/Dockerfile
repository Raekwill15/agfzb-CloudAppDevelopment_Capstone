FROM python:3.12.1-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]