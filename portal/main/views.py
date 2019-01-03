from django.shortcuts import render, get_object_or_404
from main.models import CompanyProfile, Customer
from django.shortcuts import reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from main.forms import CustomerForm, CompanyProfileForm, UserForm
from main.mlmodel.model import ml_model
import os
from django.utils.encoding import smart_str

@login_required
def index(request):
    # serialized_customers = serializers.serialize(
    #     'json', [customer for customer in Customer.objects.filter(company=CompanyProfile.objects.get(user=request.user))])
    serialized_customers = serializers.serialize(
        'json', [customer for customer in Customer.objects.all()])
    return render(request, 'main/index.html', {'customers': serialized_customers})


def company_register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_profile_form = CompanyProfileForm(data=request.POST)
        if user_form.cleaned_data.get('email') in [user.email for user in User.objects.all()]:
            return render(request, 'main/company_register.html', {'user_form_errors': 'Account with same email exists',
                                                                   'company_profile_form_errors': company_profile_form.errors})
        if user_form.is_valid() and company_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            company_profile = company_profile_form.save(commit=False)
            company_profile.user = user
            company_profile.save()

            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'main/company_register.html', {'user_form_errors': user_form.errors,
                                                                   'company_profile_form_errors': company_profile_form.errors})
        else:
            return render(request, 'main/company_register.html', {'user_form_errors': user_form.errors,
                                                               'company_profile_form_errors': company_profile_form.errors})
    return render(request, 'main/company_register.html', {})


def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'main/company_login.html', {'errors': 'Invalid Username/Password'})
    elif request.method == 'GET':
        return render(request, 'main/company_login.html', {})


@login_required
def company_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def get_serialized_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    serialized_customer = serializers.serialize('json', [customer, ])
    return render(request, 'main/customer_view.html', {'customer': serialized_customer})


@login_required
def add_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        company_profile = CompanyProfile.objects.get(user=request.user)
        if customer_form.is_valid():
            print(customer_form)
            customer = customer_form.save(commit=False)
            customer.company = company_profile

            model = ml_model()    
            education = 0
            if customer.education == 'Less than High School':
                education = 0
            elif customer.education == 'High School':
                education = 1
            elif customer.education == 'Bachelors':
                education = 2
            elif customer.education == 'Masters':
                education = 3
            elif customer.education == 'PhD':
                education = 4

            car_type = 0
            if customer.car_type == 'Mini Van':
                car_type = 0
            elif customer.car_type == 'Panel Truck':
                car_type = 1
            elif customer.car_type == 'Pickup':
                car_type = 2
            elif customer.car_type == 'Sports Car':
                car_type = 3
            elif customer.car_type == 'Van':
                car_type = 4
            elif customer.car_type == 'SUV':
                car_type = 5

            occupation = 0
            if customer.occupation == 'Clerical':
                occupation = 0
            elif customer.occupation == 'Doctor':
                occupation = 1
            elif customer.occupation == 'Home':
                occupation = 2
            elif customer.occupation == 'Lawyer':
                occupation = 3
            elif customer.occupation == 'Manager':
                occupation = 4
            elif customer.occupation == 'Professional':
                occupation = 5
            elif customer.occupation == 'Student':
                occupation = 6
            elif customer.occupation == 'Blue Collar':
                occupation = 7

            X = {}
            X['KIDSDRIV'] = customer.no_children_drive
            X['AGE'] = customer.age
            X['HOMEKIDS'] = customer.no_children
            X['INCOME'] = customer.income
            if customer.parents_alive == 'Yes':
                X['PARENT1'] = 1
            else:
                X['PARENT1'] = 0
            X['HOME_VAL'] = customer.home_estimate
            if customer.marriage_status == 'Yes':
                X['MSTATUS'] = 1
            else:
                X['MSTATUS'] = 0

            if customer.gender == 'Yes':
                X['GENDER'] = 1
            else:
                X['GENDER'] = 0
            X['TRAVTIME'] = customer.avg_travel_time
            if customer.car_use == 'Yes':
                X['CAR_USE'] = 1
            else:
                X['CAR_USE'] = 0
            X['BLUE_BOOK'] =  customer.insured_value
            if customer.car_color_red == 'Yes':
                X['RED_CAR'] = 1
            else:
                X['RED_CAR'] = 0
            X['OLD_CLAIM'] = customer.prev_insurance_amt
            X['CLM_FREQ'] = customer.prev_insurance_no
            if customer.prev_claim_revoked=='Yes':
                X['REVOKED'] = 1
            else:
                X['REVOKED'] = 0
            X['CAR_AGE'] = customer.car_age
            if customer.urbanicity == 'Yes':
                X['URBAN_CITY'] = 1
            else:
                X['URBAN_CITY'] = 0
            X['EDUCATION'] = education
            X['CAR_TYPE'] = car_type
            X['OCCUPATION'] = occupation
            customer.risk = model.predict(X)
            customer.save()

            if request.POST.get('add'):
                return HttpResponseRedirect(reverse('index'))

            elif request.POST.get('calculate'):
                return render(request, 'main/final.html', { 'id': customer.id,
                                                            'risk': model.predict(X)})
            
        else:
            # print(customer_form.errors)
            errors_json = customer_form.errors.as_json()
            return JsonResponse({'form_errors': errors_json})
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_customer(request, pk=None):
    if request.method == 'GET':
        pk = request.GET['customer_id']
        serialized_customer = ''
        try:
            customer = Customer.objects.get(pk=pk)
            serialized_customer = serializers.serialize('json', [customer, ])
            status = '200'
            return render(request, 'main/customer_edit.html', {'status': status,
                                                       'customer': serialized_customer})
        except:
            status = '404'
            return render(request, 'main/customer_edit.html', {'status': status,
                                                       'customer': serialized_customer})
    else:
        customer = Customer.objects.get(pk=pk)
        customer_edit_form = CustomerForm(request.POST, instance=customer)
        if customer_edit_form.is_valid():
            customer = customer_edit_form.save(commit=False)
            model = ml_model()    
            education = 0
            if customer.education == 'Less than High School':
                education = 0
            elif customer.education == 'High School':
                education = 1
            elif customer.education == 'Bachelors':
                education = 2
            elif customer.education == 'Masters':
                education = 3
            elif customer.education == 'PhD':
                education = 4

            car_type = 0
            if customer.car_type == 'Mini Van':
                car_type = 0
            elif customer.car_type == 'Panel Truck':
                car_type = 1
            elif customer.car_type == 'Pickup':
                car_type = 2
            elif customer.car_type == 'Sports Car':
                car_type = 3
            elif customer.car_type == 'Van':
                car_type = 4
            elif customer.car_type == 'SUV':
                car_type = 5

            occupation = 0
            if customer.occupation == 'Clerical':
                occupation = 0
            elif customer.occupation == 'Doctor':
                occupation = 1
            elif customer.occupation == 'Home':
                occupation = 2
            elif customer.occupation == 'Lawyer':
                occupation = 3
            elif customer.occupation == 'Manager':
                occupation = 4
            elif customer.occupation == 'Professional':
                occupation = 5
            elif customer.occupation == 'Student':
                occupation = 6
            elif customer.occupation == 'Blue Collar':
                occupation = 7

            X = {}
            X['KIDSDRIV'] = customer.no_children_drive
            X['AGE'] = customer.age
            X['HOMEKIDS'] = customer.no_children
            X['INCOME'] = customer.income
            if customer.parents_alive == 'Yes':
                X['PARENT1'] = 1
            else:
                X['PARENT1'] = 0
            X['HOME_VAL'] = customer.home_estimate
            if customer.marriage_status == 'Yes':
                X['MSTATUS'] = 1
            else:
                X['MSTATUS'] = 0

            if customer.gender == 'Yes':
                X['GENDER'] = 1
            else:
                X['GENDER'] = 0
            X['TRAVTIME'] = customer.avg_travel_time
            if customer.car_use == 'Yes':
                X['CAR_USE'] = 1
            else:
                X['CAR_USE'] = 0
            X['BLUE_BOOK'] =  customer.insured_value
            if customer.car_color_red == 'Yes':
                X['RED_CAR'] = 1
            else:
                X['RED_CAR'] = 0
            X['OLD_CLAIM'] = customer.prev_insurance_amt
            X['CLM_FREQ'] = customer.prev_insurance_no
            if customer.prev_claim_revoked=='Yes':
                X['REVOKED'] = 1
            else:
                X['REVOKED'] = 0
            X['CAR_AGE'] = customer.car_age
            if customer.urbanicity == 'Yes':
                X['URBAN_CITY'] = 1
            else:
                X['URBAN_CITY'] = 0
            X['EDUCATION'] = education
            X['CAR_TYPE'] = car_type
            X['OCCUPATION'] = occupation
            customer.risk = model.predict(X)
            customer.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            serialized_errors = serializers.serialize(
                'json', [customer_edit_form.errors])
            return JsonResponse({'form_errors': serialized_errors})

@login_required    
def delete_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.delete()
    return HttpResponseRedirect(reverse("index"))
