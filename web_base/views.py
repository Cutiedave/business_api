from django.shortcuts import render, HttpResponse, redirect
from base.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
#from django.utils import simplejson
from django.core import serializers
from .templates import decorators
from dotenv import load_dotenv
import requests as req
import numpy as np
import openai
import json
import os

from base.models import Business_case_data, MyUser, Lead
from base.serializers import MepSerializer, LeadSerializer

from .tasks import send_email

load_dotenv()




def business_case_data(data):
    print('Organization Biz Dev Costs:')
    data['avg_bdr_salary'] = 49500
    print('Avg BDR Salary: ${:,.2f}'.format(data['avg_bdr_salary']))
    data['avg_training_cost'] = 1252
    print('Avg BDR Training Costs: ${:,.2f}'.format(data['avg_training_cost']))
    data['benefit_cost_percent'] = .31
    data['benefit_cost'] = data['avg_bdr_salary'] * data['benefit_cost_percent']
    print('Avg BDR Benefits: ${:,.2f}'.format(data['benefit_cost']))
    data['avg_bdr_cost'] = (data['avg_bdr_salary'] + data['avg_training_cost'] + data['benefit_cost']) 
    print('Avg All-In BDR Costs: ${:,.2f}'.format(data['avg_bdr_cost']) + ' per employee')
    data['annual_bdr_costs'] = data['avg_bdr_cost']*data['sales_team_size']
    data['monthly_bdr_costs'] = data['annual_bdr_costs'] / 12
    data['hourly_bdr_cost'] = data['annual_bdr_costs'] / 2080
    data['daily_bdr_cost'] =  data['hourly_bdr_cost'] * 8
    print('Organization BDR Costs: ${:,.2f}'.format(data['annual_bdr_costs']))
    print('Organization Daily BDR Costs: ${:,.2f}'.format(data['daily_bdr_cost']))
    print('Organization Hourly BDR Costs: ${:,.2f}'.format(data['hourly_bdr_cost']))
    print('\n\n')
    
    data['monthly_work_hours'] = 40*4
    data['monthly_work_mins'] = data['monthly_work_hours'] * 60
    data['monthly_work_secs'] = data['monthly_work_mins'] * 60
    data['org_work_hours'] = data['monthly_work_hours'] * data['sales_team_size']
    data['org_work_mins'] = data['monthly_work_mins'] * data['sales_team_size']
    data['org_work_secs'] = data['monthly_work_secs'] * data['sales_team_size']
    
    print('Organization Conversion Rates:')
    print('Contacts Monthly: ' + str(data['monthly_prospects']))
    print('Leads Monthly: ' + str(data['monthly_leads']))
    data['org_prospect_conversion'] = round((data['monthly_leads']/data['monthly_prospects']), 4)
    print('Contact to Lead Rate: ' + str(data['org_prospect_conversion']*100) + '%')
    data['org_prospect_to_lead'] = np.ceil(data['monthly_prospects']/data['monthly_leads'])
    print('{:,.2f}'.format(data['org_prospect_to_lead']) + ' contacts to generate each lead')
    data['org_lead_conversion'] = data['qualified_lead_close_rate']
    data['org_lead_to_qual'] = data['monthly_qual_leads'] / data['monthly_leads']
    data['org_lead_to_qual'] = 1 / data['org_lead_to_qual']
    data['org_qual_lead_to_close'] = 1 / data['org_lead_conversion']
    data['org_lead_to_close'] = data['org_lead_to_qual'] * data['org_qual_lead_to_close']
    print('{:,.2f}'.format(data['org_lead_to_close']) + ' leads needed to generate each sale')
    
    print('\n\n')
    
    data['rev_share'] = 0.05
    data['abdd_hourly_rate'] = 6
    print('ABDD Processing Rates')
    print('ABDD Process Rate: ' + str(data['abdd_hourly_rate']) + ' contacts/hour')
    data['abdd_daily_rate'] = data['abdd_hourly_rate'] * 24
    print('ABDD Process Rate: ' + str(data['abdd_daily_rate']) + ' contacts/day')
    data['abdd_monthly_rate'] = data['abdd_daily_rate'] * 30
    print('ABDD Process Rate: ' + str(data['abdd_monthly_rate']) + ' contacts/month')
    print('\n\n')
    
    print('ABDD Software Fees')
    data['abdd_monthly_cost'] = 750
    print('ABDD Cost: ${:,.2f}'.format(data['abdd_monthly_cost']) + ' per/month')
    data['accounts_needed'] = np.ceil(data['monthly_prospects'] / data['abdd_monthly_rate'])
    print('ABDD Accounts Needed: ' + str(data['accounts_needed']))
    data['org_abdd_monthly_rate'] = data['abdd_monthly_rate'] * data['accounts_needed']
    data['org_abdd_monthly_cost'] = data['abdd_monthly_cost'] * data['accounts_needed']
    data['org_abdd_annual_cost'] = data['org_abdd_monthly_cost'] * 12
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_annual_cost']) + ' per/year')
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_monthly_cost']) + ' per/month')
    data['org_abdd_daily_cost'] = data['org_abdd_monthly_cost'] / 30
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_daily_cost']) + ' per/day')
    data['org_abdd_hourly_cost'] = data['org_abdd_daily_cost'] / 24
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_hourly_cost']) + ' per/hour')
    data['org_abdd_min_cost'] = data['org_abdd_hourly_cost'] / 60
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_min_cost']) + ' per/minute')
    data['org_abdd_sec_cost'] = data['org_abdd_min_cost'] / 60
    print('Organization ABDD Cost: ${:,.2f}'.format(data['org_abdd_sec_cost']) + ' per/second')
    print('\n\n')
    
    
    #Orgaizational Cost Savings
    print('Organizational Savings')
    data['bdr_vs_abbd_monthly_savings'] = (data['monthly_bdr_costs'] - data['abdd_monthly_rate'])
    print('Organization Savings: ${:,.2f}'.format(data['bdr_vs_abbd_monthly_savings']) + ' per/month')
    data['savings_percent'] = round((data['bdr_vs_abbd_monthly_savings'] / data['monthly_bdr_costs'])*100, 2)
    data['bdr_vs_abbd_annual_savings'] = (data['annual_bdr_costs'] - (data['abdd_monthly_rate']*12))
    print('Organization Savings: ${:,.2f}'.format(data['bdr_vs_abbd_annual_savings']) + ' per/year')
    print('Organization Savings Rate: ' + str(data['savings_percent']) + '%')
    print('\n\n')
    
    #Contact processing rates
    print('Contact Processing Rates:')
    data['team_monthly_rate'] = data['monthly_prospects']
    print('Organization: ' + str(data['team_monthly_rate']) + ' contacts/month')
    data['team_weekly_rate'] = data['team_monthly_rate'] / 4
    print('Organization: ' + str(data['team_weekly_rate']) + ' contacts/week')
    data['team_daily_rate'] = data['team_weekly_rate'] / 5
    print('Organization: ' + str(data['team_daily_rate']) + ' contacts/day')
    data['team_hourly_rate'] = data['team_daily_rate'] / 8
    print('Organization: ' + str(data['team_hourly_rate']) + ' contacts/hour')
    data['team_process_rate'] = np.ceil(60 / data['team_hourly_rate'])
    print('Team Process Rate: ' + str(data['team_process_rate']) + ' mins/contact')
    
    data['ind_monthly_rate'] = data['team_monthly_rate'] / data['sales_team_size']
    print('Individual Process Rate: ' + str(data['ind_monthly_rate']) + ' contacts/month')
    data['ind_weekly_rate'] = data['team_weekly_rate'] / data['sales_team_size']
    print('Individual Process Rate: ' + str(data['ind_weekly_rate']) + ' contacts/week')
    data['ind_daily_rate'] = data['team_daily_rate'] / data['sales_team_size']
    print('Individual Process Rate: ' + str(data['ind_daily_rate']) + ' contacts/day')
    data['ind_hourly_rate'] = data['team_hourly_rate'] / data['sales_team_size']
    print('Individual Process Rate: ' + str(data['ind_hourly_rate']) + ' contacts/hour')
    data['ind_process_rate'] = np.ceil(data['team_process_rate'] * data['sales_team_size'])
    print('Inidividual Process Rate: ' + str(data['ind_process_rate']) + ' mins/lead')
    print('\n')
    
    
    # speed rate
    data['org_abdd_process_ratio'] = round(data['org_abdd_monthly_rate'] / data['monthly_prospects'], 2)
    data['ind_abdd_process_ratio'] = round(data['abdd_monthly_rate'] / data['ind_monthly_rate'], 2)
    print('ABDD Processess Contacts ' + str(data['org_abdd_process_ratio']) + 'x Faster than your current organization.')
    print('Single ABDD Subscription Processess Contacts ' + str(data['ind_abdd_process_ratio']) + 'x Faster than a single BDR on your team.')
    print('\n\n')
    
    #Unfruitful processing rates
    print('Time Spent on Unfruitful Contacts')
    data['unfruitful_contact_rate'] = (data['monthly_prospects'] - data['monthly_leads'])/data['monthly_prospects']
#     print(str(round(unfruitful_contact_rate*100, 2)) + '% of attempts made from BDR team are unsuccessful.')
    data['team_monthly_unfruitful'] = data['monthly_prospects'] - data['monthly_leads']
#     print('Organization Unfruitful Contacts: ' + str(team_monthly_unfruitful) + ' per/month')
    data['team_daily_unfruitful'] = data['team_monthly_unfruitful'] / 20
#     print('Organization Unfruitful Contacts: ' + str(team_daily_unfruitful) + ' per/month')
    data['team_hourly_unfruitful'] = data['team_daily_unfruitful'] / 8
#     print('Organization Unfruitful Contacts: ' + str(team_hourly_unfruitful) + ' per/month')
    
    data['ind_monthly_unfruitful'] = data['team_monthly_unfruitful'] / data['sales_team_size']
#     print('Individual Unfruitful Contacts: ' + str(ind_monthly_unfruitful) + ' per/month')
    data['ind_daily_unfruitful'] = data['team_daily_unfruitful'] / data['sales_team_size']
#     print('Individual Unfruitful Contacts: ' + str(ind_daily_unfruitful) + ' per/month')
    data['ind_hourly_unfruitful'] = data['team_hourly_unfruitful'] / data['sales_team_size']
#     print('Individual Unfruitful Contacts: ' + str(ind_hourly_unfruitful) + ' per/month')
    
    #Unfruitful processing costs
    data['team_monthly_unfruitful_costs'] = data['unfruitful_contact_rate'] * data['monthly_bdr_costs']
#     print('Organization Unfruitful Costs: ${:,.2f}'.format(team_monthly_unfruitful_costs) + ' per/month')
    data['team_hourly_unfruitful_costs'] = data['unfruitful_contact_rate'] * data['hourly_bdr_cost']
#     print('Organization Unfruitful Costs: ${:,.2f}'.format(team_hourly_unfruitful_costs) + ' per/hour')
    data['team_daily_unfruitful_costs'] = data['team_hourly_unfruitful_costs'] * 8
#     print('Organization Unfruitful Costs: ${:,.2f}'.format(team_daily_unfruitful_costs) + ' per/day')
    
    
    data['ind_monthly_unfruitful_costs'] = data['team_monthly_unfruitful_costs'] / data['sales_team_size']
#     print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_monthly_unfruitful_costs) + ' per/month')
    data['ind_daily_unfruitful_costs'] = data['team_daily_unfruitful_costs'] / data['sales_team_size']
#     print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_daily_unfruitful_costs) + ' per/day')
    data['ind_hourly_unfruitful_costs'] = data['team_hourly_unfruitful_costs'] / data['sales_team_size']
#     print('Individual Unfruitful Costs: ${:,.2f}'.format(ind_hourly_unfruitful_costs) + ' per/hour')
    print('\n\n')
        
        
        
    #Lead generation rates
    print('Lead conversion rates.')
    data['team_days_per_lead'] = 20 / data['monthly_leads']
#     print('Organization Lead Generation Rate: {:,.2f}'.format(data['team_days_per_lead']) + ' days per lead')
    data['team_hours_per_lead'] = data['team_days_per_lead'] * 8
#     print('Organization Lead Generation Rate: {:,.2f}'.format(data['team_hours_per_lead']) + ' hours per lead')
    data['team_mins_per_lead'] = data['team_hours_per_lead'] * 60
#     print('Organization Lead Generation Rate: {:,.0f}'.format(team_mins_per_lead) + ' minutes per lead')
    data['team_secs_per_lead'] = data['team_mins_per_lead'] * 60
#     print('Organization Lead Generation Rate: {:,.0f}'.format(team_secs_per_lead) + ' seconds per lead')
    
    data['ind_days_per_lead'] = data['team_days_per_lead'] * data['sales_team_size']
#     print('Individual Lead Generation Rate: {:,.2f}'.format(ind_days_per_lead) + ' days per lead')
    data['ind_hours_per_lead'] = data['team_hours_per_lead'] * data['sales_team_size']
#     print('Individual Lead Generation Rate: {:,.2f}'.format(ind_hours_per_lead) + ' hours per lead')
    data['ind_mins_per_lead'] = data['team_mins_per_lead'] * data['sales_team_size']
#     print('Individual Lead Generation Rate: {:,.0f}'.format(ind_mins_per_lead) + ' minutes per lead')
    data['ind_secs_per_lead'] = data['team_secs_per_lead'] * data['sales_team_size']
#     print('Individual Lead Generation Rate: {:,.0f}'.format(ind_secs_per_lead) + ' seconds per lead')
#     print('\n\n')
    
    #ABDD conversion rates
    print('ABDD Conversion Rates')
    #abdd lead rate = number of contacts to lead / contact_reach_rate
    data['abdd_lead_rate_monthly'] = data['org_abdd_monthly_rate'] / data['org_prospect_to_lead']
    print('ABDD Lead Generation Rate: {:,.2f}'.format(data['abdd_lead_rate_monthly']) + ' leads per month')
    data['abdd_cpl'] = data['org_abdd_monthly_cost'] / data['abdd_lead_rate_monthly']
    
    
    
    
    #Lead costs
    data['contact_data_cost'] = data['org_prospect_to_lead'] * data['contact_cost']
    data['lead_bdr_cost'] = data['hourly_bdr_cost'] * data['team_hours_per_lead']
    data['lead_cost'] = data['contact_cost'] + data['lead_bdr_cost']
    print('Organization Avg. Cost Per Lead: ${:,.2f}'.format(data['lead_cost']))
    print('ABDD Avg. Cost Per Lead: ${:,.2f}'.format(data['abdd_cpl']))
    data['cpl_savings'] = data['lead_cost'] - data['abdd_cpl']
    data['cpl_reduction'] = round((data['cpl_savings'] / data['lead_cost'])*100, 2)
    print('CPL Reduction: ' + str(data['cpl_reduction']) + '%')
    print('\n\n')
    
    
    
    #Time to generate sell
    #determine lead to sell conversion rate
    print('Sell Generation Rates')
    data['org_sell_gen_day'] = data['org_lead_to_close'] * data['team_days_per_lead']
#     print('Organization Sell Generation Rate: {:,.2f}'.format(org_sell_gen_day) + ' days to generate likely sellable lead')
    data['org_sell_gen_hour'] = data['org_lead_to_close'] * data['team_hours_per_lead']
#     print('Organization Sell Generation Rate: {:,.2f}'.format(org_sell_gen_hour) + ' hour to generate likely sellable lead')
    data['org_sell_gen_min'] = data['org_lead_to_close'] * data['team_mins_per_lead']
#     print('Organization Sell Generation Rate: {:,.0f}'.format(org_sell_gen_min) + ' mins to generate likely sellable lead')
    data['org_sell_gen_sec'] = data['org_lead_to_close'] * data['team_secs_per_lead']
#     print('Organization Sell Generation Rate: {:,.0f}'.format(org_sell_gen_sec) + ' secs to generate likely sellable lead')
    
    data['ind_sell_gen_day'] = data['org_sell_gen_day'] * data['sales_team_size']
#     print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_day) + ' days to generate likely sellable lead')
    data['ind_sell_gen_hour'] = data['org_sell_gen_hour'] * data['sales_team_size']
#     print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_hour) + ' hours to generate likely sellable lead')
    data['ind_sell_gen_min'] = data['org_sell_gen_min'] * data['sales_team_size']
#     print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_min) + ' minutes to generate likely sellable lead')
    data['ind_sell_gen_sec'] = data['org_sell_gen_sec'] * data['sales_team_size']
#     print('Individual Sell Generation Rate: {:,.0f}'.format(ind_sell_gen_sec) + ' seconds to generate likely sellable lead')
#     print('\n\n')
    
    
    print('Sell Generation Costs')
    #cost per likely sell = number of leads * cost per lead
    data['cost_per_likely_sell'] = data['org_lead_to_close'] * data['lead_cost']
    print('Avg. Organization BDR Cost to Generate Sale: ${:,.2f}'.format(data['cost_per_likely_sell']))
    #ABDD cost per sell
    #CPS = number of leads needed * cost per lead
    data['abdd_cps'] = (data['org_lead_to_close'] * data['abdd_cpl']) + (data['rev_share'] * data['avg_deal_size'])
    print('Avg. ABDD Cost to Generate Sale: ${:,.2f}'.format(data['abdd_cps']))

    return (data)


# Create your views here.
def home(request):
    return render(request,'web_base/home.html')

def dashboard_detail(requests,id):
    users=Business_case_data.objects.filter(id=id).first()
    if not users:
        messages.error(requests, 'No data available, please fill the data form')
        return redirect('home_web_base')
    data=MepSerializer(users).data
    data['prospect_report'] = data['prospect_report'].replace('Paragraph ', '')
    return render(requests, 'web_base/table_page.html',{'data':data})



# logic view
def seller_form(requests):
    if requests.method=='POST':
        if os.environ.get('mode', 'PRODUCTION') == 'PRODUCTION':
            dashboard_link = f"https://{requests.META['HTTP_HOST']}/dashboard"
        else:
            dashboard_link = f"http://{requests.META['HTTP_HOST']}/dashboard"

        data =  {
        'seller_first_name': requests.POST.get('firstName'),
        'seller_last_name': requests.POST.get('lastName'),
        'seller_name': requests.POST.get('firstName')+ ' '+requests.POST.get('lastName'),
        'seller_phone': requests.POST.get('phoneNumber'),
        'seller_email': requests.POST.get('email'),
        'email': requests.POST.get('email'),


        'seller_company': requests.POST.get('companyName'),
        'seller_position': requests.POST.get('position'),

        'services_sold':requests.POST.get('services_sold'),

        'lead_email': requests.POST.get('email'),
        'lead_position': requests.POST.get('lead_position'),
        
        'role': requests.POST.get('role'),
        'size': requests.POST.get('size'),
        'industry': requests.POST.get('industry'),

        'seller_overview':requests.POST.get('seller_overview'),
        'social_proof':requests.POST.get('social_proof'),
        'short_social_proof':requests.POST.get('short_social_proof'),
        'seller_offer':requests.POST.get('seller_offer'),

        'seller_sales_cycle': float(requests.POST.get('averageSalesCycle')),
        'sales_team_size': float(requests.POST.get('peopleInYourOrganisation')),
        'monthly_prospects': float(requests.POST.get('howManyProspects')),
        'monthly_leads': float(requests.POST.get('howManyLeads')),
        'monthly_qual_leads': float(requests.POST.get('howManyQualifiedLeads')),
        'qualified_lead_close_rate': float(requests.POST.get('teamCloseRate')),
        'avg_deal_size': float(requests.POST.get('averageDealSize')),
        'contact_cost': float(requests.POST.get('prospectcontactcost')),
        'contact_channels': requests.POST.get('contacting'),


        'averageSalesCycle': float(requests.POST.get('averageSalesCycle')),
        'peopleInYourOrganisation': float(requests.POST.get('peopleInYourOrganisation')),
        'howManyProspects': float(requests.POST.get('howManyProspects')),
        'howManyLeads': float(requests.POST.get('howManyLeads')),
        'howManyQualifiedLeads': float(requests.POST.get('howManyQualifiedLeads')),
        'teamCloseRate': float(requests.POST.get('teamCloseRate')),
        'averageDealSize': float(requests.POST.get('averageDealSize')),
        'prospectcontactcost': float(requests.POST.get('prospectcontactcost')),
        'contacting': requests.POST.get('contacting'),
        'dashboard_link': dashboard_link

        }

        pw = 'default'
        full_name = data['seller_first_name'] + ' ' + data['seller_last_name']

        # checks if the data has been previously saved
        if (Business_case_data.objects.filter(email=data['email']).exists()==True):
            messages.error(requests, 'Data already saved with this email, please check dashboard')
            return redirect('home_web_base')         
            
        # saves a user
        userform=MyUser.objects.create_user(email=data['email'],password=pw,full_name=full_name)
        userform.save()

        if (Lead.objects.filter(user_mail=data['email']).exists()==True):
            lead=Lead.objects.filter(user_mail=data['email']).first()
            lead_info=LeadSerializer(lead)

            data['lead_full_name'] = lead_info['lead_full_name']
            data['lead_full_name_possesive'] = lead_info['lead_full_name_possesive']
            data['lead_interest'] = lead_info['lead_interest']
            data['lead_social_links'] = lead_info['lead_social_links']
            data['lead_experience'] = lead_info['lead_experience']
            data['company_city'] = lead_info['company_city']
            data['company_state'] = lead_info['company_state']
            data['company_site'] = lead_info['company_site']
            data['company'] = lead_info['company']
            data['lead_skills'] = lead_info['lead_skills']
            data['lead_position'] = lead_info['lead_position']

        else:
            ES_QUERY = {"query": {"bool": {"must": [
                        {"term": {"job_title_levels": str(data['lead_position'])}},
                        {"term": {"job_company_industry": str(data['industry'])}},
                        {"term": {"job_company_size": str(data['size'])}},
                        {"term": {"job_title_role": str(data['role'])}},
                        {"term": {"location_country": "united states"}},
                        {"exists": {"field": "phone_numbers"}},
                        {"exists": {"field": "work_email"}},
                        {"exists": {"field": "mobile_phone"}}
                        ]}}}
            API_KEY = os.environ.get('API_KEY', '*****')
            PDL_URL = os.environ.get('PDL_URL', 'https://api.peopledatalabs.com/v5/person/search')
            request_header = {"Content-Type": "application/json", "X-api-key": API_KEY}
            params = {"dataset": "all", "query": json.dumps(ES_QUERY), "size": 1, "pretty": True }
            response = req.get(PDL_URL, headers=request_header, params=params).json()
            if response['status'] == 200:
                lead_info = response['data'][0]

                if isinstance(lead_info['location_metro'], float):
                    company_city = ''
                else:
                    company_city = lead_info['location_metro']

                if isinstance(lead_info['location_region'], float):
                    company_state = ''
                else:
                    company_state = lead_info['location_region']

                if isinstance(lead_info['job_company_website'], float):
                    company_site = ''
                else:
                    company_site = lead_info['job_company_website']

                if isinstance(lead_info['job_title'], float):
                    lead_info_position = data['lead_position']
                else:
                    lead_info_position = lead_info['job_title']

                if isinstance(lead_info['interests'], float):
                    lead_info_interest = ''
                else:
                    lead_info_interest = lead_info['interests']

                if isinstance(lead_info['skills'], float):
                    lead_info_skills = ''
                else:
                    lead_info_skills = lead_info['skills']

                experience = []
                for item in lead_info['experience']:
                    it = item['company']
                    exp_company = it['name']
                    if exp_company == None:
                        exp_company = '[]'
                    exp_size = it['size']
                    if exp_size == None:
                        exp_size = '[]'
                    exp_industry = it['industry']
                    if exp_industry == None:
                        exp_industry = '[]'
                    exp_website = it['website']
                    if exp_website == None:
                        exp_website = '[]'
                    exp_start = item['start_date']
                    if exp_start == None:
                        exp_start = '[]'
                    exp_end = item['end_date']
                    if exp_end == None:
                        exp_end = '[]'
                    it_title = item['title']
                    exp_title = it_title['name']
                    if exp_title == None:
                        exp_title = '[]'
                    exp_review = (exp_title + ' at ' + exp_company + ' start date: ' + exp_start + ' end date: ' + exp_end
                                + ' website: ' + exp_website)
                    experience.append(exp_review)

        
                lead_social_links = []
                try:
                    if len(lead_info['linkedin_url']) > 0:
                        lead_social_links.append(lead_info['linkedin_url'])
                except:
                    pass
                try:
                    if len(lead_info['facebook_url']) > 0:
                        lead_social_links.append(lead_info['facebook_url'])
                except:
                    pass
                data['lead_full_name'] = lead_info['full_name']
                data['lead_full_name_possesive'] = data['lead_full_name'] + "'s'"
                data['lead_interest'] = lead_info_interest 
                data['lead_social_links'] = lead_social_links
                data['lead_experience'] = experience
                data['company_city'] = company_city
                data['company_state'] = company_state
                data['company_site'] = company_site
                data['company'] = lead_info['job_company_name']
                data['lead_skills']= lead_info_skills
                data['lead_position'] = lead_info_position

            else:
                messages.error(requests, f"Unable to gather lead data: {response['error']['message']}")
                return render(requests, 'web_base/home.html')
            
            print(data['company_city'])
            lead=Lead(
                    user_mail = data['email'],
                    lead_full_name = data['lead_full_name'] ,
                    lead_full_name_possesive = data['lead_full_name_possesive'],
                    lead_interest = data['lead_interest'],
                    lead_social_links = data['lead_social_links'],
                    lead_experience = data['lead_experience'],
                    company_city = data['company_city'],
                    company_state = data['company_state'],
                    company_site = data['company_site'],
                    company = data['company'],
                    lead_skills = data['lead_skills'],
                    lead_position = data['lead_position'],
                )
            lead.save()






        print('Seller: ' + data['seller_first_name'] + ' ' + data['seller_last_name'])
        print('Seller Company: ' + data['seller_company'])
        print('Avg. Sales Cycle: ' + str(data['seller_sales_cycle']) + ' months')
        print('BDRs: ' + str(data['sales_team_size']))
        print('Monthly Prospects Contacted: ' + str(data['monthly_prospects']))
        print('Monthly Leads Generated: ' + str(data['monthly_leads']))
        print('Monthly Qualified Leads: ' + str(data['monthly_qual_leads']))
        print('Qualified Close Rate: ' + str(data['qualified_lead_close_rate'] * 100) + '%')
        print('Average Deal: $' + str(data['avg_deal_size']))
        print('Contact Channels: ' + str(data['contact_channels']))
        print('Contact Cost: $' + str(data['contact_cost']))
        
        # generates business variables
        business_data = business_case_data(data)

        # send tasks to celery
        send_email.apply_async(args=[
                business_data
            ], retry=True
        )

        data_instance = Business_case_data(
                user = userform,
                lead = lead, 
                Rev_share=business_data['rev_share'],
                email=data['email'],

                Accounts_needed=business_data['accounts_needed'],

                Avg_BDR_Salary=business_data['avg_bdr_salary'], 
                Avg_BDR_Training_Costs=business_data['avg_training_cost'], 
                Avg_BDR_Benefits=business_data['benefit_cost'], 

                # BDR costs
                Annual_Organization_BDR_Costs=business_data['annual_bdr_costs'], 
                Daily_Organization_BDR_Costs=business_data['daily_bdr_cost'], 
                Hourly_Organization_BDR_Costs=business_data['hourly_bdr_cost'], \
                Monthly_Organization_BDR_Costs = business_data['monthly_bdr_costs'],

                # ABDD costs
                ABDD_cost_per_year=business_data['org_abdd_annual_cost'], 
                ABDD_cost_per_month=business_data['org_abdd_monthly_cost'], 
                ABDD_cost_per_day=business_data['org_abdd_daily_cost'], 
                ABDD_cost_per_hour=business_data['org_abdd_hourly_cost'], 
                ABDD_cost_per_minute=business_data['org_abdd_min_cost'], 
                ABDD_cost_per_second=business_data['org_abdd_sec_cost'], 

                # BDR lead/contact info
                Contacts_Monthly=business_data['monthly_prospects'], 
                Contacts_Daily=business_data['team_daily_rate'], 
                Contacts_Hourly=business_data['team_hourly_rate'], 
                Leads_Monthly=business_data['monthly_leads'], 
                contacts_to_generate_each_lead=business_data['org_prospect_to_lead'], 
                Contact_to_Lead_Rate=business_data['org_prospect_conversion'], 
                leads_needed_to_generate_each_sale=business_data['org_lead_to_close'], \
                Organization_Avg_Cost_Per_Lead=business_data['lead_cost'],
                
                # ABDD lead/contact info
                ABDD_contacts_per_hour=business_data['abdd_hourly_rate'], 
                ABDD_contacts_per_day=business_data['abdd_daily_rate'], 
                ABDD_contacts_per_month=business_data['abdd_monthly_rate'], \
                ABDD_Lead_Generation_Rate=business_data['abdd_lead_rate_monthly'],
                ABDD_Avg_Cost_Per_Lead=business_data['abdd_cpl'],
                
                # savings
                savings_per_month=business_data['bdr_vs_abbd_monthly_savings'], savings_per_year=business_data['bdr_vs_abbd_annual_savings'], 
                saving_rate=business_data['savings_percent'],

                # unfruitful
                unfruitful_contact_rate=business_data['unfruitful_contact_rate'], organization_unfruitful_contacts_monthly=business_data['team_monthly_unfruitful'], 
                organization_unfruitful_contacts_daily=business_data['team_daily_unfruitful'], organization_unfruitful_contacts_hourly=business_data['team_hourly_unfruitful'],
                organization_unfruitful_costs_monthly=business_data['team_monthly_unfruitful_costs'], 
                organization_unfruitful_costs_hourly=business_data['team_hourly_unfruitful_costs'], 
                organization_unfruitful_costs_daily=business_data['team_daily_unfruitful_costs'],

                # speed
                org_abdd_process_ratio = business_data['org_abdd_process_ratio'],
                ind_abdd_process_ratio = business_data['ind_abdd_process_ratio'],

                # sale BDR
                Avg_Organization_BDR_Cost_to_Generate_Sale=business_data['cost_per_likely_sell'],

                # sale ABDD
                Avg_ABDD_Cost_to_Generate_Sale=business_data['abdd_cps'],


                # cost per lead reduction
                CPL_Reduction=business_data['cpl_reduction'],

                # time to generate leads BDR
                Organization_Lead_Generation_Rate_daily=business_data['team_days_per_lead'], 
                Organization_Lead_Generation_Rate_hourly=business_data['team_hours_per_lead'], 

                # time to generate leads ABDD
                ABDD_Lead_Generation_Rate_daily=20 / business_data['abdd_lead_rate_monthly'], 
                #ABDD_Lead_Generation_Rate_hourly=business_data['team_hours_per_lead'], 

                Organization_Sell_Generation_Rate=business_data['org_sell_gen_day'],
                dashboard_link = data['dashboard_link'],
                seller_name=business_data['seller_name'], company=business_data['seller_company']
        )
        data_instance.dashboard_link = f"{data['dashboard_link']}/{data_instance.id}/"
        data_instance.save()

        output_data = Business_case_data.objects.filter(id=data_instance.id).first()
        if not output_data:
            messages.error(requests, 'No data available, please fill the data form')
            return redirect('home_web_base')
        serializer=MepSerializer(output_data)
        return render(requests, 'web_base/table_page.html',{'data':serializer.data})

    else:
        messages.error(requests, 'error: invalid dashboard link')
        return redirect('home_web_base')


@decorators.unauthenticated_user
def Login(requests):
    if requests.user.is_authenticated:
        return redirect('home_web_base')
    
    if requests.method=='POST':
        email=requests.POST.get('email').lower()
        password=requests.POST.get('password')

        try:
            user= MyUser.objects.get(email=email)
        except:
            messages.error(requests, 'Invalid user')
            return render(requests, 'web_base/login_page.html')
            
        user = authenticate(requests, email=email, password=password)

        if user is None:
            messages.error(requests, 'password is incorrect')
            return render(requests, 'web_base/login_page.html')
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
        pw = requests.POST.get('password')
        email = requests.POST.get('email').lower()
        full_name = requests.POST.get('Full name').capitalize()
        # pw2=requests.POST.get('confirm_password')
        # if pw != pw2:
        #     messages.error(requests, 'password mismatch')

            # return render(requests,'web_base/signup.html')

        if (MyUser.objects.filter(email=email).exists()==True):
             messages.error(requests, 'username already exists')
             return render(requests,'web_base/login_page.html')           
            
        userform=MyUser.objects.create_user(email=email,password=pw,full_name=full_name)
        #if userform.is_valid():
        userform.save()

        messages.success(requests,'Account successfully created, please login')
        return redirect('login')
        # else:
        #     messages.error(requests, 'invalid details')
        #     return redirect('login')
    return render(requests,'web_base/login_page.html', {'color':'blues'})

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
