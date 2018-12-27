from django.shortcuts import render, get_object_or_404
from main.models import CompanyProfile, Customer
from django.shortcuts import reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from main.forms import CustomerForm, CompanyProfileForm, UserForm
#from main.mlmodel.model import ml_model


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
    return render(request, 'main/customer_view.html', {'customer': serialized_customer})


@login_required
def add_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        company_profile = CompanyProfile.objects.get(user=request.user)
        if customer_form.is_valid():
            print(customer_form)
            customer = customer_form.save(commit=False)
            #model = ml_model()
            #risk = model.predict(X)
            customer.company = company_profile
            customer.risk = 0
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
        try:
            customer = Customer.objects.get(pk=pk)
            serialized_customer = serializers.serialize('json', [customer, ])
            status = '200'
        except:
            status = '404'
    else:
        customer = Customer.objects.get(pk=pk)
        customer_edit_form = CustomerForm(request.POST, instance=customer)
        if customer_edit_form.is_valid():
            customer_edit_form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            serialized_errors = serializers.serialize(
                'json', [customer_edit_form.errors])
            return JsonResponse({'form_errors': serialized_errors})
    return render(request, 'main/customer_edit.html', {'status': status,
                                                       'customer': serialized_customer})
