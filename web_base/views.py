from django.shortcuts import render, HttpResponse, redirect
from base.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.utils import simplejson
from django.core import serializers
from .templates import decorators
from dotenv import load_dotenv
import requests as req
import numpy as np
import json
import os

load_dotenv()


# Create your views here.
def home(request):
    return render(request,'web_base/home.html')


def seller_form(requests):
    #if requests.user.is_authenticated:
    if requests.method=='POST':

        data = {
        'user':None,
        'firstName': requests.POST.get('firstName'),
        'lastName': requests.POST.get('lastName'),
        'seller_name': requests.POST.get('firstName')+ ' '+requests.POST.get('lastName'),
        'phoneNumber': requests.POST.get('phoneNumber'),
        'email': requests.POST.get('email'),
        'lead_email': requests.POST.get('email'),
        'companyName': requests.POST.get('companyName'),
        'position': requests.POST.get('position'),


        'level': requests.POST.get('level'),
        'role': requests.POST.get('role'),
        'size': requests.POST.get('size'),
        'industry': requests.POST.get('industry'),

        'averageSalesCycle': float(requests.POST.get('averageSalesCycle')),
        'peopleInYourOrganisation': float(requests.POST.get('peopleInYourOrganisation')),
        'howManyProspects': float(requests.POST.get('howManyProspects')),
        'howManyLeads': float(requests.POST.get('howManyLeads')),
        'howManyQualifiedLeads': float(requests.POST.get('howManyQualifiedLeads')),
        'teamCloseRate': float(requests.POST.get('teamCloseRate')),
        'averageDealSize': float(requests.POST.get('averageDealSize')),
        'prospectcontactcost': float(requests.POST.get('prospectcontactcost')),
        'contacting': requests.POST.get('contacting'),

        }

#         if os.environ.get('mode')=='DEVELOPMENT':
#             base_url='http://localhost:8000'
#         else:
#             base_url=os.environ.get('BASE_DOMAIN','http://localhost:8000')
#         url=f'{base_url}/api/v1/webhook/'
        url='https://businessapi-production.up.railway.app/api/v1/webhook/'


        res = req.post( url, json=data)
        data = res.json()



        return render(requests, 'web_base/table_page.html', {'data':data})

            

            
            # return redirect('seller_form')

    # else:
    #     return redirect('login')
    else:
#         if os.environ.get('mode')=='DEVELOPMENT':
#             base_url='http://localhost:8000'
#         else:
#             base_url=os.environ.get('BASE_DOMAIN','http://localhost:8000')

#         url=f'{base_url}/api/v1/detail/'
        url='https://businessapi-production.up.railway.app/api/v1/detail/'

        res = req.get(url)
        data = res.json()

        return render(requests, 'web_base/table_page.html', {'data':data})


@decorators.unauthenticated_user
def Login(requests):
    if requests.user.is_authenticated:
        return redirect('home_web_base')
    
    if requests.method=='POST':
        username=requests.POST.get('username').lower()
        password=requests.POST.get('password')

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(requests, 'Invalid user')

        user = authenticate(requests, username=username, password=password)

        if user is None:
            messages.error(requests, 'password is incorrect')
        else:
            login(requests, user)
            return redirect('home_web_base')
    
    return render(requests, 'web_base/login_page.html')


def Logout(request):
    logout(request)
    return redirect('home_web_base')

@decorators.unauthenticated_user
def register(requests):
    if requests.user.is_authenticated:
        return redirect('home_web_base')

    if requests.method=='POST':
        #user=UserCreationForm(requests.POST)
        pw=requests.POST.get('password')
        pw2=requests.POST.get('confirm_password')
        if pw != pw2:
            messages.error(requests, 'password mismatch')

            return render(requests,'web_base/signup.html')
        if (User.objects.filter(username=requests.POST.get('username')).exists()==True):
             messages.error(requests, 'username already exists')
             return render(requests,'web_base/signup.html')           
            
        userform=User.objects.create_user(username=requests.POST.get('username').lower(),password=requests.POST.get('password'),first_name=requests.POST.get('First Name'), email=requests.POST.get('email'))
        #if userform.is_valid():
        userform.save()

        messages.success(requests,'Account successfully created')
        return redirect('login')
        # else:
        #     messages.error(requests, 'invalid details')
        #     return redirect('login')
    return render(requests,'web_base/signup.html')

# def profile(request,pk):
#     return HttpResponse('welcome '+User.objects.get(id=pk).username)

# @login_required(login_url='/login')
# # def userlist(request):
# #     return HttpResponse(serializers.serialize('json', User.objects.all()), content_type='application/json')
# #     #return render(request , 'base/user_list.html',{'users':User.objects.all()})
# def userlist(request):
#     data=requests.get('http://fhir-api:8080/Patient')
#     return HttpResponse(json.dumps(data.json()),content_type="application/json")
#     #return render(request , 'base/user_list.html',{'users':User.objects.all()})

# def patientlist(request):
#     data=requests.get('http://fhir-api:8080/Patient')
#     data=data.json()
#     try:
#         data = {'id':[x ['resource']['id'] for x in data['entry']]}
#         return HttpResponse(json.dumps(data),content_type="application/json")
#     except:
#         return HttpResponse(json.dumps({}),content_type="application/json")
#     #return render(request , 'base/user_list.html',{'users':User.objects.all()})

# def patient_id(request):
#     idd=request.GET['id']
#     data=requests.get('http://fhir-api:8080/Patient/'+idd)
#     data=data.json()
#     return HttpResponse(json.dumps(data),content_type="application/json")
#     #return render(request , 'base/user_list.html',{'users':User.objects.all()})

# def delete_patient(request):
#     if request.method == 'POST':
#         idd=request.POST['id']
#         data=requests.delete('http://fhir-api:8080/Patient/'+idd)
#         return HttpResponse('record deleted')
#     else:
#         return render(request, 'base/delete.html')        

# def update(request):
#     if request.method == 'POST':
#         idd = request.POST['id']
#         first_name=request.POST['name']
#         family_name=request.POST['family_name']
#         gender=request.POST['gender']
#         phone=request.POST['phone']
#         state=request.POST['state']
#         data = {
#             "resourceType":"Patient",
#             "id":idd,
#             "active":state,
#             "gender":gender,
#             "name":[{"family":family_name,"given":first_name}],
#             "telecom": [{"system":"phone","value":phone,"use":"home_web_base"}]
#         }
#         data=requests.put('http://fhir-api:8080/Patient/'+idd,json = data)
#         return HttpResponse('record updated')
#     else:
#         return render(request, 'base/update.html')


# def update_patient(request):
#     if request.method == 'POST':
#         idd = request.POST['id']
#         data=requests.get('http://fhir-api:8080/Patient/'+idd).json()
#         if data["resourceType"]== "Patient":
#             data={
#                 "id":idd,
#                 "first_name":data['name'][0]['given'][0],
#                 "family_name":data['name'][0]['family'],
#                 "gender":data['gender'],
#                 "phone":data["telecom"][0]['value'],
#                 "state":str(data['active']).lower()
#             }

#             return render(request,'base/update.html',data)
#         else:
#             return HttpResponse('Invalid ID')
#     else:
#         return render(request, 'base/update_n.html') 


# def add_patient(request):
#     if request.method == 'POST':
#         first_name=request.POST['name']
#         family_name=request.POST['family_name']
#         gender=request.POST['gender']
#         phone=request.POST['phone']
#         state=request.POST['state']
#         data = {
#             "resourceType":"Patient",
#             "active":state,
#             "gender":gender,
#             "name":[{"family":family_name,"given":first_name}],
#             "telecom": [{"system":"phone","value":phone,"use":"home_web_base"}]
#         }
#         data=requests.post('http://fhir-api:8080/Patient/',json = data)
#         return HttpResponse('record added')
#     else:
#         return render(request, 'base/create.html') 
