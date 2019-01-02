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

- Training the ML Model For the First Time

  - Uncomment the following lines of code in portal/main/mlmodel/model.py

    ```python
    # model = ml_model()
    # model.train()
    ```

  - Run the script

    ```bash
    python portal/main/mlmodel/model.py
    ```

- Run Server

```bash
python manage.py runserver
```

- Demonstration

  - Dummy Company
    - Username: amul
    - Password: password