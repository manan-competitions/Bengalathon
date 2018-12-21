# Bengalathon 2019

- Setting up the virtual environment

```bash
cd Bengalathon
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- Migrating the Database

```bash
cd portal
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

- Run Server

```bash
python manage.py runserver
```
