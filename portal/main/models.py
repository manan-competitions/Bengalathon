from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


NO_CHILDREN_CHOICE = [(i, i) for i in range(11)]
MARRIAGE_CHOICE = (('Unmarried', 'Unmarried'),
                   ('Married', 'Married'))
GENDER_CHOICE = (('Female', 'Female'),
                 ('Male', 'Male'),
                 ('Other', 'Other'))
EDUCATION_CHOICE = (('Less than High School', 'Less than High School'),
                    ('High School', 'High School'),
                    ('Bachelors', 'Bachelors'),
                    ('Masters', 'Masters'),
                    ('PhD', 'PhD'))
OCCUPATION_CHOICE = (('Manager', 'Manager'),
                     ('Doctor', 'Doctor'),
                     ('Student', 'Student'),
                     ('Blue Collar', 'Blue Collar'),
                     ('Lawyer', 'Lawyer'),
                     ('Clerical', 'Clerical'),
                     ('Professional', 'Professional'),
                     ('Home', 'Home'))
CARTYPE_CHOICE = (('Van', 'Van'),
                  ('Panel Truck', 'Panel Truck'),
                  ('Minivan', 'Minivan'),
                  ('Sports', 'Sports'),
                  ('SUV', 'SUV'),
                  ('Pickup', 'Pickup'))


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE)
    name = models.CharField('Customer Name', max_length=100)
    dob = models.DateField()
    age = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], default=1)
    no_children = models.IntegerField(choices=NO_CHILDREN_CHOICE)
    no_children_drive = models.IntegerField(choices=NO_CHILDREN_CHOICE)
    income = models.IntegerField(default=0)
    parents_alive = models.BooleanField(default=False)
    home_estimate = models.IntegerField(default=0)
    marriage_status = models.CharField(
        'Marriage Status', choices=MARRIAGE_CHOICE, max_length=100)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=100)
    education = models.CharField(choices=EDUCATION_CHOICE, max_length=100)
    occupation = models.CharField(choices=OCCUPATION_CHOICE, max_length=100)
    avg_travel_time = models.IntegerField(default=0)
    car_use = models.CharField(
        choices=(('Commercial', 'Commercial'), ('Private', 'Private')), max_length=100)
    car_type = models.CharField(choices=CARTYPE_CHOICE, max_length=100)
    car_color_red = models.BooleanField(default=False)
    car_age = models.IntegerField(default=0)
    urbanicity = models.CharField(
        choices=(('Rural', 'Rural'), ('Urban', 'Urban')), max_length=100)
    risk = models.FloatField(default=0.0, validators=[MaxValueValidator(1.0)])

    def __str__(self):
        return self.name
