<img align="right" src="https://bengalathon.wb.gov.in/application/public/images/bengalathon.png" height=90>

# Bengalathon 2019 (Deep Claims)


## Introduction
This Repository 

## Screenshots

## Machine Learning Model 
### Data pre processing
The Data obtained had:
* Missing values 
* A mix of continuous and categorical features
* Large disparities in the range of features

We tried a variety of techniques to combat these shortcomings:
* Regression to fill in continuous missing values
* Random Forest Classifiers to fill in categorical missing values
* One-hot encoding for the categorical features
* Logarithmic/Adaptive binning to convert the continuous features into categorical features
* Feature Scaling (min-max)
* Auto-encoders to get a small amount of meaningful parameters from the original Dataset 
### ML Architecture
We found that an ensemble of ML models outperformed the rest of the models.

## Website 

## Installing
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


## License
<img align="right" src="https://www.gnu.org/graphics/gplv3-88x31.png">
GNU GENERAL PUBLIC LICENSE

Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies

of this license document, but changing it is not allowed.
