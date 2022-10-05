# Django bookshop microservice

### Bookshop (Django) + Warehouse(Django Rest Framework)  

- auth system;
- cart based on session;
- live status updates of books and orders;
- reviews;
- messages;
- email notification;
- filter, sorting, search;
- contact form;
- celery, celery beat;
- flower, swagger, pgadmin;


You will need to do that for launch:
1) Create "**.env**" in the 'shop/core' with this data:

```
DEBUG=
SECRET_KEY=''

CELERY_BROKER='redis://redis:6379/0'
CELERY_BACKEND='redis://redis:6379/0'

DB_NAME=shop
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db_shop
DB_PORT=5432
TOKEN_KEY='' #You will need that for connection with stock.
```

2) Create "**.env**" in the 'stock/core' with this data:
```
DEBUG=
SECRET_KEY=
```
3) Run  
```
docker-compose build
docker-compose up
```
