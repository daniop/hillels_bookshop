FROM python:3.10

COPY ./stock/requirements.txt /

RUN pip install -r requirements.txt

COPY ./stock/ /app

WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]