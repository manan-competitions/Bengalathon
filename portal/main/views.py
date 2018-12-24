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

@login_required
def index(request):
    serialized_customers = serializers.serialize(
        'json', [customer for customer in Customer.objects.all()])
    return render(request, 'main/index.html', {'customers': serialized_customers})


def company_register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_profile_form = CompanyProfileForm(data=request.POST)

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
                return render(request, 'main/company_login.html', {'user_form_errors': user_form.errors,
                                                                   'company_profile_form_errors': company_profile_form.errors})
        else:
            return render(request, 'main/company_login.html', {'user_form_errors': user_form.errors,
                                                                'company_profile_form_errors': company_profile_form.errors})
    return render(request, 'main/company_login.html', {})


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
    return JsonResponse({'customer': serialized_customer})


@login_required
def add_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        company_profile = CompanyProfile.objects.get(user=request.user)
        if customer_form.is_valid():
            print(customer_form)
            customer_form_data = customer_form.cleaned_data
            customer = Customer()
            customer.company = company_profile
            customer.name = customer_form_data['name']
            customer.dob = customer_form_data['dob']
            customer.age = customer_form_data['age']
            customer.no_children = customer_form_data['no_children']
            customer.no_children_drive = customer_form_data['no_children_drive']
            customer.income = customer_form_data['income']
            customer.parents_alive = customer_form_data['parents_alive']
            customer.home_estimate = customer_form_data['home_estimate']
            customer.marriage_status = customer_form_data['marriage_status']
            customer.gender = customer_form_data['gender']
            customer.education = customer_form_data['education']
            customer.occupation = customer_form_data['occupation']
            customer.avg_travel_time = customer_form_data['avg_travel_time']
            customer.car_use = customer_form_data['car_use']
            customer.car_type = customer_form_data['car_type']
            customer.car_color_red = customer_form_data['car_color_red']
            customer.car_age = customer_form_data['car_age']
            customer.urbanicity = customer_form_data['urbanicity']
            model = ml_model()
            risk = model.predict(X)
            customer.risk = risk
            customer.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            # print(customer_form.errors)
            errors_json = customer_form.errors.as_json()
            return JsonResponse({'form_errors': errors_json})
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_customer(request, pk=None):
    if request.method == 'GET':
        pk = request.GET['customer_id']
        customer = get_object_or_404(Customer, pk=pk)
        serialized_customer = serializers.serialize('json', [customer, ])
    else:
        customer = get_object_or_404(Customer, id=pk)
        customer_edit_form = CustomerForm(request.POST, instance=customer)
        if customer_edit_form.is_valid():
            customer_edit_form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            serialized_errors = serializers.serialize(
                'json', [customer_edit_form.errors])
            return JsonResponse({'form_errors': serialized_errors})
    return render(request, 'main/customer_edit.html', {'customer': serialized_customer})
