from django import forms
from django.contrib.auth.models import User
from main.models import Customer, CompanyProfile


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'dob', 'age', 'no_children', 'no_children_drive', 'income', 'parents_alive', 'home_estimate', 'marriage_status',
                  'gender', 'education', 'occupation', 'avg_travel_time', 'car_use', 'car_type', 'car_color_red', 'car_age', 'urbanicity',
                  'insured_value', 'prev_insurance_amt', 'prev_insurance_no', 'prev_claim_revoked')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ('name',)
