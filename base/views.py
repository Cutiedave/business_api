import re
import json
import numpy as np
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions, status
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view

from django.http import JsonResponse

from .models import Business_case_data
from .serializers import MepSerializer




#1.0 Import modules
# from googleapiclient import sample_tools
# from googleapiclient.http import build_http

# import os, csv, time, html5lib, requests, logging, sys, math, tda, asyncio, random, smtplib
# import numpy as np
# import pandas as pd
# import ujson as json
# import json
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# from playsound import playsound
# import ssl, shutil
# from requests import get
# from bs4 import BeautifulSoup
# from ast import literal_eval

# import openai, chronological
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
# #import org.openqa.selenium.JavascriptExecutor



# import datetime as dt
# from datetime import date
# from datetime import datetime
# from twilio.rest import Client
# from email.message import EmailMessage
# pd.options.mode.chained_assignment = None

# from dotenv import load_dotenv
# load_dotenv()

# gmb_un = os.environ.get('gmb_un')
# gmb_pw = os.environ.get('gmb_pw')
# oai_sk = os.environ.get('oai_sk')
# oai_org_id = os.environ.get('oai_org_id')
# twilio_sid = os.environ.get('twilio_sid')
# twilio_token = os.environ.get('twilio_token')

# email_auth = os.environ.get('email_auth')
# email1 = os.environ.get('email1')
# email1_pw = os.environ.get('email1_pw')
# typeform_pat = os.environ.get('typeform_pat')
# pdl_key = os.environ.get('pdl_key')
# form_res = os.environ.get('form_res')
# form = os.environ.get('form')
# PDL_URL = os.environ.get('PDL_URL')

# account_sid = twilio_sid
# auth_token = twilio_token
# twil_client = Client(account_sid, auth_token)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.csrf import ensure_csrf_cookieprospect


def get_basic_info(requests):
    jsondata = requests.body
    last_res = json.loads(jsondata)

    # response = data
    # last_res = response['form_response']['answers']

    #----------------------------------------------------------------------------------------------------------------
    
    #execute email/text send
    #run_live = True
    run_live = False

    # Set seller information
    seller_first_name = last_res["firstName"]
    seller_last_name = last_res["lastName"]
    seller_phone = last_res["phoneNumber"]
    seller_email = last_res["email"]
    lead_email = seller_email
    seller_company = last_res["companyName"]
    seller_position = last_res["position"]

    seller_sales_cycle = int(last_res["averageSalesCycle"])
    sales_team_size = int(last_res["peopleInYourOrganisation"])
    monthly_prospects = int(last_res["howManyProspects"])
    monthly_leads = int(last_res["howManyLeads"])
    monthly_qual_leads = int(last_res["howManyQualifiedLeads"])
    qualified_lead_close_rate = int(last_res["teamCloseRate"])/100
    avg_deal_size = int(last_res["averageDealSize"])
    contact_channels = str(last_res["contacting"])
    # contact_channels = contact_channels.replace("'", "")
    # contact_channels = contact_channels.replace("[", "")
    # contact_channels = contact_channels.replace("]", "")
    #contact_cost = float(last_res[23]["text"])
    contact_cost = float(last_res["prospectContactInfo"])

    print('Seller: ' + seller_first_name + ' ' + seller_last_name)
    print('Seller Company: ' + seller_company)
    print('Avg. Sales Cycle: ' + str(seller_sales_cycle) + ' months')
    print('BDRs: ' + str(sales_team_size))
    print('Monthly Prospects Contacted: ' + str(monthly_prospects))
    print('Monthly Leads Generated: ' + str(monthly_leads))
    print('Monthly Qualified Leads: ' + str(monthly_qual_leads))
    print('Qualified Close Rate: ' + str(qualified_lead_close_rate * 100) + '%')
    print('Average Deal: $' + str(avg_deal_size))
    print('Contact Channels: ' + str(contact_channels))
    print('Contact Cost: $' + str(contact_cost))

    return (sales_team_size, monthly_prospects, monthly_leads, monthly_qual_leads, contact_cost, 
                       qualified_lead_close_rate, avg_deal_size, seller_first_name + ' ' + seller_last_name, seller_company)


def business_case_data(sales_team_size, monthly_prospects, monthly_leads, monthly_qual_leads, contact_cost, 
                       qualified_lead_close_rate, avg_deal_size, seller_name, seller_company):
    print('Organization Biz Dev Costs:')
    avg_bdr_salary = 49500
    print('Avg BDR Salary: ${:,.2f}'.format(avg_bdr_salary))
    avg_training_cost = 1252
    print('Avg BDR Training Costs: ${:,.2f}'.format(avg_training_cost))
    benefit_cost_percent = .31
    benefit_cost = avg_bdr_salary * benefit_cost_percent
    print('Avg BDR Benefits: ${:,.2f}'.format(benefit_cost))
    avg_bdr_cost = (avg_bdr_salary + avg_training_cost + benefit_cost) 
    print('Avg All-In BDR Costs: ${:,.2f}'.format(avg_bdr_cost) + ' per employee')
    annual_bdr_costs = avg_bdr_cost*sales_team_size
    monthly_bdr_costs = annual_bdr_costs / 12
    hourly_bdr_cost = annual_bdr_costs / 2080
    daily_bdr_cost = hourly_bdr_cost * 8
    print('Organization BDR Costs: ${:,.2f}'.format(annual_bdr_costs))
    print('Organization Daily BDR Costs: ${:,.2f}'.format(daily_bdr_cost))
    print('Organization Hourly BDR Costs: ${:,.2f}'.format(hourly_bdr_cost))
    print('\n\n')
    
    monthly_work_hours = 40*4
    monthly_work_mins = monthly_work_hours * 60
    monthly_work_secs = monthly_work_mins * 60
    org_work_hours = monthly_work_hours * sales_team_size
    org_work_mins = monthly_work_mins * sales_team_size
    org_work_secs = monthly_work_secs * sales_team_size
    
    print('Organization Conversion Rates:')
    print('Contacts Monthly: ' + str(monthly_prospects))
    print('Leads Monthly: ' + str(monthly_leads))
    org_prospect_conversion = round((monthly_leads/monthly_prospects), 4)
    print('Contact to Lead Rate: ' + str(org_prospect_conversion*100) + '%')
    org_prospect_to_lead = np.ceil(monthly_prospects/monthly_leads)
    print('{:,.2f}'.format(org_prospect_to_lead) + ' contacts to generate each lead')
    org_lead_conversion = qualified_lead_close_rate
    org_lead_to_qual = monthly_qual_leads / monthly_leads
    org_lead_to_qual = 1 / org_lead_to_qual
    org_qual_lead_to_close = 1 / org_lead_conversion
    org_lead_to_close = org_lead_to_qual * org_qual_lead_to_close
    print('{:,.2f}'.format(org_lead_to_close) + ' leads needed to generate each sale')
    
    print('\n\n')
    
    rev_share = 0.05
    abdd_hourly_rate = 6
    print('ABDD Processing Rates')
    print('ABDD Process Rate: ' + str(abdd_hourly_rate) + ' contacts/hour')
    abdd_daily_rate = abdd_hourly_rate * 24
    print('ABDD Process Rate: ' + str(abdd_daily_rate) + ' contacts/day')
    abdd_monthly_rate = abdd_daily_rate * 30
    print('ABDD Process Rate: ' + str(abdd_monthly_rate) + ' contacts/month')
    print('\n\n')
    
    print('ABDD Software Fees')
    abdd_monthly_cost = 750
    print('ABDD Cost: ${:,.2f}'.format(abdd_monthly_cost) + ' per/month')
    accounts_needed = np.ceil(monthly_prospects / abdd_monthly_rate)
    print('ABDD Accounts Needed: ' + str(accounts_needed))
    org_abdd_monthly_rate = abdd_monthly_rate * accounts_needed
    org_abdd_monthly_cost = abdd_monthly_cost * accounts_needed
    org_abdd_annual_cost = org_abdd_monthly_cost * 12
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_annual_cost) + ' per/year')
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_monthly_cost) + ' per/month')
    org_abdd_daily_cost = org_abdd_monthly_cost / 30
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_daily_cost) + ' per/day')
    org_abdd_hourly_cost = org_abdd_daily_cost / 24
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_hourly_cost) + ' per/hour')
    org_abdd_min_cost = org_abdd_hourly_cost / 60
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_min_cost) + ' per/minute')
    org_abdd_sec_cost = org_abdd_min_cost / 60
    print('Organization ABDD Cost: ${:,.2f}'.format(org_abdd_sec_cost) + ' per/second')
    print('\n\n')
    
    
    #Orgaizational Cost Savings
    print('Organizational Savings')
    bdr_vs_abbd_monthly_savings = (monthly_bdr_costs - abdd_monthly_rate)
    print('Organization Savings: ${:,.2f}'.format(bdr_vs_abbd_monthly_savings) + ' per/month')
    savings_percent = round((bdr_vs_abbd_monthly_savings / monthly_bdr_costs)*100, 2)
    bdr_vs_abbd_annual_savings = (annual_bdr_costs - (abdd_monthly_rate*12))
    print('Organization Savings: ${:,.2f}'.format(bdr_vs_abbd_annual_savings) + ' per/year')
    print('Organization Savings Rate: ' + str(savings_percent) + '%')
    print('\n\n')
    
    #Contact processing rates
    print('Contact Processing Rates:')
    team_monthly_rate = monthly_prospects
    print('Organization: ' + str(team_monthly_rate) + ' contacts/month')
    team_weekly_rate = team_monthly_rate / 4
    print('Organization: ' + str(team_weekly_rate) + ' contacts/week')
    team_daily_rate = team_weekly_rate / 5
    print('Organization: ' + str(team_daily_rate) + ' contacts/day')
    team_hourly_rate = team_daily_rate / 8
    print('Organization: ' + str(team_hourly_rate) + ' contacts/hour')
    team_process_rate = np.ceil(60 / team_hourly_rate)
    print('Team Process Rate: ' + str(team_process_rate) + ' mins/contact')
    
    ind_monthly_rate = team_monthly_rate / sales_team_size
    print('Individual Process Rate: ' + str(ind_monthly_rate) + ' contacts/month')
    ind_weekly_rate = team_weekly_rate / sales_team_size
    print('Individual Process Rate: ' + str(ind_weekly_rate) + ' contacts/week')
    ind_daily_rate = team_daily_rate / sales_team_size
    print('Individual Process Rate: ' + str(ind_daily_rate) + ' contacts/day')
    ind_hourly_rate = team_hourly_rate / sales_team_size
    print('Individual Process Rate: ' + str(ind_hourly_rate) + ' contacts/hour')
    ind_process_rate = np.ceil(team_process_rate * sales_team_size)
    print('Inidividual Process Rate: ' + str(ind_process_rate) + ' mins/lead')
    print('\n')
    
    org_abdd_process_ratio = round(org_abdd_monthly_rate / monthly_prospects, 2)
    ind_abdd_process_ratio = round(abdd_monthly_rate / ind_monthly_rate, 2)
    print('ABDD Processess Contacts ' + str(org_abdd_process_ratio) + 'x Faster than your current organization.')
    print('Single ABDD Subscription Processess Contacts ' + str(ind_abdd_process_ratio) + 'x Faster than a single BDR on your team.')
    print('\n\n')
    
    #Unfruitful processing rates
    print('Time Spent on Unfruitful Contacts')
    unfruitful_contact_rate = (monthly_prospects - monthly_leads)/monthly_prospects
    print(str(round(unfruitful_contact_rate*100, 2)) + '% of attempts made from BDR team are unsuccessful.')
    team_monthly_unfruitful = monthly_prospects - monthly_leads
    print('Organization Unfruitful Contacts: ' + str(team_monthly_unfruitful) + ' per/month')
    team_daily_unfruitful = team_monthly_unfruitful / 20
    print('Organization Unfruitful Contacts: ' + str(team_daily_unfruitful) + ' per/month')
    team_hourly_unfruitful = team_daily_unfruitful / 8
    print('Organization Unfruitful Contacts: ' + str(team_hourly_unfruitful) + ' per/month')
    
    ind_monthly_unfruitful = team_monthly_unfruitful / sales_team_size
    print('Individual Unfruitful Contacts: ' + str(ind_monthly_unfruitful) + ' per/month')
    ind_daily_unfruitful = team_daily_unfruitful / sales_team_size
    print('Individual Unfruitful Contacts: ' + str(ind_daily_unfruitful) + ' per/month')
    ind_hourly_unfruitful = team_hourly_unfruitful / sales_team_size
    print('Individual Unfruitful Contacts: ' + str(ind_hourly_unfruitful) + ' per/month')
    
    #Unfruitful processing costs
    team_monthly_unfruitful_costs = unfruitful_contact_rate * monthly_bdr_costs
    print('Organization Unfruitful Costs: ${:,.2f}'.format(team_monthly_unfruitful_costs) + ' per/month')
    team_hourly_unfruitful_costs = unfruitful_contact_rate * hourly_bdr_cost
    print('Organization Unfruitful Costs: ${:,.2f}'.format(team_hourly_unfruitful_costs) + ' per/hour')
    team_daily_unfruitful_costs = team_hourly_unfruitful_costs * 8
    print('Organization Unfruitful Costs: ${:,.2f}'.format(team_daily_unfruitful_costs) + ' per/day')
    
    
    ind_monthly_unfruitful_costs = team_monthly_unfruitful_costs / sales_team_size
    print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_monthly_unfruitful_costs) + ' per/month')
    ind_daily_unfruitful_costs = team_daily_unfruitful_costs / sales_team_size
    print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_daily_unfruitful_costs) + ' per/day')
    ind_hourly_unfruitful_costs = team_hourly_unfruitful_costs / sales_team_size
    print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_hourly_unfruitful_costs) + ' per/hour')
    print('\n\n')
        
        
        
    #Lead generation rates
    print('Lead conversion rates.')
    team_days_per_lead = 20 / monthly_leads
    print('Organization Lead Generation Rate: {:,.2f}'.format(team_days_per_lead) + ' days per lead')
    team_hours_per_lead = team_days_per_lead * 8
    print('Organization Lead Generation Rate: {:,.2f}'.format(team_hours_per_lead) + ' hours per lead')
    team_mins_per_lead = team_hours_per_lead * 60
    print('Organization Lead Generation Rate: {:,.0f}'.format(team_mins_per_lead) + ' minutes per lead')
    team_secs_per_lead = team_mins_per_lead * 60
    print('Organization Lead Generation Rate: {:,.0f}'.format(team_secs_per_lead) + ' seconds per lead')
    
    ind_days_per_lead = team_days_per_lead * sales_team_size
    print('Individual Lead Generation Rate: {:,.2f}'.format(ind_days_per_lead) + ' days per lead')
    ind_hours_per_lead = team_hours_per_lead * sales_team_size
    print('Individual Lead Generation Rate: {:,.2f}'.format(ind_hours_per_lead) + ' hours per lead')
    ind_mins_per_lead = team_mins_per_lead * sales_team_size
    print('Individual Lead Generation Rate: {:,.0f}'.format(ind_mins_per_lead) + ' minutes per lead')
    ind_secs_per_lead = team_secs_per_lead * sales_team_size
    print('Individual Lead Generation Rate: {:,.0f}'.format(ind_secs_per_lead) + ' seconds per lead')
    print('\n\n')
    
    #ABDD conversion rates
    print('ABDD Conversion Rates')
    #abdd lead rate = number of contacts to lead / contact_reach_rate
    abdd_lead_rate_monthly = org_abdd_monthly_rate / org_prospect_to_lead
    print('ABDD Lead Generation Rate: {:,.2f}'.format(abdd_lead_rate_monthly) + ' leads per month')
    abdd_cpl = org_abdd_monthly_cost / abdd_lead_rate_monthly
    
    
    
    
    #Lead costs
    contact_data_cost = org_prospect_to_lead * contact_cost
    lead_bdr_cost = hourly_bdr_cost * team_hours_per_lead
    lead_cost = contact_cost + lead_bdr_cost
    print('Organization Avg. Cost Per Lead: ${:,.2f}'.format(lead_cost))
    print('ABDD Avg. Cost Per Lead: ${:,.2f}'.format(abdd_cpl))
    cpl_savings = lead_cost - abdd_cpl
    cpl_reduction = round((cpl_savings / lead_cost)*100, 2)
    print('CPL Reduction: ' + str(cpl_reduction) + '%')
    print('\n\n')
    
    #Business Case Synopsis 
    ##### Current State
    #Annual & Monthly employee costs, contact processing rate, lead generation rate
    
    
    #Time to generate sell
    #determine lead to sell conversion rate
    print('Sell Generation Rates')
    org_sell_gen_day = org_lead_to_close * team_days_per_lead
    print('Organization Sell Generation Rate: {:,.2f}'.format(org_sell_gen_day) + ' days to generate likely sellable lead')
    org_sell_gen_hour = org_lead_to_close * team_hours_per_lead
    print('Organization Sell Generation Rate: {:,.2f}'.format(org_sell_gen_hour) + ' hour to generate likely sellable lead')
    org_sell_gen_min = org_lead_to_close * team_mins_per_lead
    print('Organization Sell Generation Rate: {:,.0f}'.format(org_sell_gen_min) + ' mins to generate likely sellable lead')
    org_sell_gen_sec = org_lead_to_close * team_secs_per_lead
    print('Organization Sell Generation Rate: {:,.0f}'.format(org_sell_gen_sec) + ' secs to generate likely sellable lead')
    
    ind_sell_gen_day = org_sell_gen_day * sales_team_size
    print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_day) + ' days to generate likely sellable lead')
    ind_sell_gen_hour = org_sell_gen_hour * sales_team_size
    print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_hour) + ' hours to generate likely sellable lead')
    ind_sell_gen_min = org_sell_gen_min * sales_team_size
    print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_min) + ' minutes to generate likely sellable lead')
    ind_sell_gen_sec = org_sell_gen_sec * sales_team_size
    print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_sec) + ' seconds to generate likely sellable lead')
    print('\n\n')
    
    
    print('Sell Generation Costs')
    #cost per likely sell = number of leads * cost per lead
    cost_per_likely_sell = org_lead_to_close * lead_cost
    print('Avg. Organization BDR Cost to Generate Sale: ${:,.2f}'.format(cost_per_likely_sell))
    #ABDD cost per sell
    #CPS = number of leads needed * cost per lead
    abdd_cps = (org_lead_to_close * abdd_cpl) + (rev_share * avg_deal_size)
    print('Avg. ABDD Cost to Generate Sale: ${:,.2f}'.format(abdd_cps))






    return ({"Rev_share":rev_share ,"accounts_needed":accounts_needed ,"avg_bdr_salary":avg_bdr_salary, "avg_training_cost":avg_training_cost, "benefit_cost":benefit_cost, "annual_bdr_costs":annual_bdr_costs, "daily_bdr_cost":daily_bdr_cost, "hourly_bdr_cost":hourly_bdr_cost, \
            
            "monthly_prospects":monthly_prospects, "monthly_leads":monthly_leads, "org_prospect_conversion":org_prospect_conversion*100, "org_prospect_to_lead":org_prospect_to_lead, "org_lead_to_close":org_lead_to_close, \
            
            "abdd_hourly_rate":abdd_hourly_rate, "abdd_daily_rate":abdd_daily_rate, "abdd_monthly_rate":abdd_monthly_rate, \
            
            "org_abdd_annual_cost":org_abdd_annual_cost, "org_abdd_monthly_cost":org_abdd_monthly_cost, "org_abdd_daily_cost":org_abdd_daily_cost, "org_abdd_hourly_cost":org_abdd_hourly_cost, "org_abdd_min_cost":org_abdd_min_cost, "org_abdd_sec_cost":org_abdd_sec_cost, 

            "bdr_vs_abbd_monthly_savings":bdr_vs_abbd_monthly_savings, "bdr_vs_abbd_annual_savings":bdr_vs_abbd_annual_savings, "savings_percent":savings_percent,


            "unfruitful_contact_rate":unfruitful_contact_rate*100, "team_monthly_unfruitful":team_monthly_unfruitful, "team_daily_unfruitful":team_daily_unfruitful,"team_hourly_unfruitful":team_hourly_unfruitful,


            "team_monthly_unfruitful_costs":team_monthly_unfruitful_costs, "team_hourly_unfruitful_costs":team_hourly_unfruitful_costs, "team_daily_unfruitful_costs":team_daily_unfruitful_costs,

            "team_days_per_lead":team_days_per_lead, "team_hours_per_lead":team_hours_per_lead, 

            "abdd_lead_rate_monthly":abdd_lead_rate_monthly, "lead_cost":lead_cost, "abdd_cpl":abdd_cpl, "cpl_reduction":cpl_reduction,

            "org_sell_gen_day":org_sell_gen_day,

            "cost_per_likely_sell":cost_per_likely_sell, "abdd_cps":abdd_cps,

            "seller_name":seller_name, "seller_company":seller_company}
            )



@csrf_exempt
@csrf_protect
@api_view(['POST'])
def get_response_typeform(requests):
    sales_team_size, monthly_prospects, monthly_leads, monthly_qual_leads, contact_cost, qualified_lead_close_rate, avg_deal_size,seller_name, seller_company = get_basic_info(requests)

    
    
    business_data = business_case_data(sales_team_size, monthly_prospects, monthly_leads, monthly_qual_leads, contact_cost, 
                   qualified_lead_close_rate, avg_deal_size, seller_name, seller_company)
    
    Business_case_data.objects.create(
            Rev_share=business_data['Rev_share'],
            Accounts_needed=business_data['accounts_needed'],
            Avg_BDR_Salary=business_data['avg_bdr_salary'], Avg_BDR_Training_Costs=business_data['avg_training_cost'], 
            Avg_BDR_Benefits=business_data['benefit_cost'], Annual_Organization_BDR_Costs=business_data['annual_bdr_costs'], 
            Daily_Organization_BDR_Costs=business_data['daily_bdr_cost'], Hourly_Organization_BDR_Costs=business_data['hourly_bdr_cost'], \
            
            Contacts_Monthly=business_data['monthly_prospects'], Leads_Monthly=business_data['monthly_leads'], 
            Contact_to_Lead_Rate=business_data['org_prospect_conversion'], contacts_to_generate_each_lead=business_data['org_prospect_to_lead'], 
            
            leads_needed_to_generate_each_sale=business_data['org_lead_to_close'], \
            
            ABDD_contacts_per_hour=business_data['abdd_hourly_rate'], ABDD_contacts_per_day=business_data['abdd_daily_rate'], 
            
            ABDD_contacts_per_month=business_data['abdd_monthly_rate'], \
            
            ABDD_cost_per_year=business_data['org_abdd_annual_cost'], ABDD_cost_per_month=business_data['org_abdd_monthly_cost'], 
            
            ABDD_cost_per_day=business_data['org_abdd_daily_cost'], ABDD_cost_per_hour=business_data['org_abdd_hourly_cost'], 
            
            ABDD_cost_per_minute=business_data['org_abdd_min_cost'], ABDD_cost_per_second=business_data['org_abdd_sec_cost'], 

            savings_per_month=business_data['bdr_vs_abbd_monthly_savings'], savings_per_year=business_data['bdr_vs_abbd_annual_savings'], 
            
            saving_rate=business_data['savings_percent'],


            unfruitful_contact_rate=business_data['unfruitful_contact_rate'], organization_unfruitful_contacts_monthly=business_data['team_monthly_unfruitful'], 
            
            organization_unfruitful_contacts_daily=business_data['team_daily_unfruitful'], organization_unfruitful_contacts_hourly=business_data['team_hourly_unfruitful'],


            organization_unfruitful_costs_monthly=business_data['team_monthly_unfruitful_costs'], 
            
            organization_unfruitful_costs_hourly=business_data['team_hourly_unfruitful_costs'], 
            
            organization_unfruitful_costs_daily=business_data['team_daily_unfruitful_costs'],

            Organization_Lead_Generation_Rate_daily=business_data['team_days_per_lead'], 
            
            Organization_Lead_Generation_Rate_hourly=business_data['team_hours_per_lead'], 

            ABDD_Lead_Generation_Rate=business_data['abdd_lead_rate_monthly'], Organization_Avg_Cost_Per_Lead=business_data['lead_cost'], 
            
            ABDD_Avg_Cost_Per_Lead=business_data['abdd_cpl'], CPL_Reduction=business_data['cpl_reduction'],

            Organization_Sell_Generation_Rate=business_data['org_sell_gen_day'],

            Avg_Organization_BDR_Cost_to_Generate_Sale=business_data['cost_per_likely_sell'], Avg_ABDD_Cost_to_Generate_Sale=business_data['abdd_cps'],

            seller_name=business_data['seller_name'], company=business_data['seller_company']
    )

    print(business_data)

    users=Business_case_data.objects.last()
    serializer=MepSerializer(users)
    
    
    #business_data['Access-Control-Allow-Origin'] = 'https://30b4-213-255-147-146.ngrok-free.app'
    return Response(serializer.data)
    

class BusinessListView(generics.ListAPIView):
    queryset = Business_case_data.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MepSerializer
    def get(self, request, *args, **kwargs):
        business_data = Business_case_data.objects.all()
        serializer = MepSerializer(business_data, many=True, context={"request":request})
        return Response(serializer.data)
    
@api_view(['GET'])
def BusinessDetailView(request,pk):
    users=Business_case_data.objects.get(user=pk)
    serializer=MepSerializer(users)
    return Response(serializer.data)

@api_view(['GET'])
def BusinessDetailView2(request):
    users=Business_case_data.objects.last()
    serializer=MepSerializer(users)
    return Response(serializer.data)
    

@api_view(['GET'])
def get_data(requests):

    return Response({'jjsjsks':'sjsksk'})


