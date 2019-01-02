from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


YES_NO_CHOICE = (('Yes', 'Yes'),('No', 'No'))
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
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], default=1)
    no_children = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    no_children_drive = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    income = models.FloatField(default=0)
    parents_alive = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    home_estimate = models.FloatField(default=0)
    marriage_status = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    gender = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    education = models.CharField(choices=EDUCATION_CHOICE, max_length=100)
    occupation = models.CharField(choices=OCCUPATION_CHOICE, max_length=100)
    avg_travel_time = models.IntegerField(default=0)
    car_use = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    car_type = models.CharField(choices=CARTYPE_CHOICE, max_length=100)
    car_color_red = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    car_age = models.IntegerField(default=0)
    urbanicity = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    insured_value = models.FloatField(default=0)
    prev_insurance_amt = models.FloatField(default=0)
    prev_insurance_no = models.IntegerField(default=0)
    prev_claim_revoked = models.CharField(max_length=3, choices=YES_NO_CHOICE)
    risk = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
