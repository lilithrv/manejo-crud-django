# Talento Digital - CRUD Python

A company dedicated to real estate rental is looking to create a web site where users can review properties available for lease, separated by commune and region. The website will have two types of users: tenants and owners.

## Dependencies

- [Django](https://www.djangoproject.com/) 5.0.7 version
- Requirements specified in requirements.txt file

## To visualize the project

- Create virtual environment

```python
python -m venv nombre_entorno
```

- Activate virtual environment

```python
source nombre_entorno/Scripts/activate
```

- Install Django

```python
pip install django
```

- Install Postgresql

```python
pip install psycopg2
```

- Install decouple (environment variables)

```python
pip install python-decouple
```

## Environment variables

Connects django app to the PostgreSQL server. To specify which database to connect to, create an `.env` file with the following structure, also available in the `.env.example` file.

```
.env

SECRET_KEY=
DEBUG=True
PG_NAME=
PG_USER=
PG_PASSWORD=
PG_HOST=
PG_PORT=
```

To migrate models:

```python
python manage.py makemigrations
python manage.py migrate
```
