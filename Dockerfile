FROM python:3.10

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONBUFFERED=1

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]