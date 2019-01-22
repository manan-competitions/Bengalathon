<img align="right" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/bengalathon.png" height=90>

# Bengalathon 2019 (Deep Claims)


## Introduction
**Problem Statement:** How can insurers leverage on historical and real-time
data to predict future claims more effectively?

* We created a web-based portal which can be used to effectively access our ML model.
* The customer details can be entered using the 'Add' option and the customer details are saved to our Database.
* The customer is then evaluated by our ML model and is assigned a credibility score and classified as 'Credible' or 'Not Credible'.
* Previous Customers can also be seen and Customer details an be modified using the 'Edit' option.
* The ML model can easily be retrained once new customer data is obtained.

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
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/model_arch.png" height=270>
</p>
It was observed that some customers were harder to classify than others. Thus, we made a semi-automatic model which passed such hard customers to the experts (Human Intervention). This led to a significant increase in accuracy.
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/acc.png" height=270>
</p>

## Website
* Login Portal
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/web_login.png" height=270>
</p>

* Home Screen
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/web_home.png" height=270>
</p>

* Adding a new Customer
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/web_add_1.png" height=270>
</p>

<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/web_add_2.png" height=270>
</p>

* Customer Details
<p>
<img align="center" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/web_details.png" height=270>
</p>

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
  - Run Server
```bash
python manage.py runserver
```
- Demonstration
  - Dummy Company
    - Username: amul
    - Password: password

## License
<img align="right" src="https://github.com/MananSoni42/Bengalathon/blob/readme/imgs/gplv3.png">
GNU GENERAL PUBLIC LICENSE

Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies

of this license document, but changing it is not allowed.
