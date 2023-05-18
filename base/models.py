from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Business_case_data(models.Model):

    user= models.OneToOneField(User, null=True , on_delete=models.CASCADE)
    Avg_BDR_Salary = models.FloatField()
    Avg_BDR_Training_Costs = models.CharField(max_length=250)
    Avg_BDR_Benefits = models.CharField(max_length=100)
    Annual_Organization_BDR_Costs = models.FloatField()
    Daily_Organization_BDR_Costs = models.FloatField()
    Hourly_Organization_BDR_Costs = models.FloatField()

    # conversion rates
    Contacts_Monthly = models.FloatField()
    Leads_Monthly = models.FloatField()
    Contact_to_Lead_Rate = models.FloatField()
    contacts_to_generate_each_lead = models.FloatField()
    leads_needed_to_generate_each_sale = models.FloatField()

    #ABDD processing rates
    ABDD_contacts_per_hour = models.FloatField()
    ABDD_contacts_per_day = models.FloatField()
    ABDD_contacts_per_month = models.FloatField()

    #ABDD costs
    ABDD_cost_per_year = models.FloatField()
    ABDD_cost_per_month = models.FloatField()
    ABDD_cost_per_day = models.FloatField()
    ABDD_cost_per_hour = models.FloatField()
    ABDD_cost_per_minute = models.FloatField()
    ABDD_cost_per_second = models.FloatField()

    # orgainzation saving
    savings_per_month = models.FloatField()
    savings_per_year = models.FloatField()
    saving_rate = models.FloatField()

    #unfruitful contacts
    unfruitful_contact_rate = models.FloatField()
    organization_unfruitful_contacts_monthly = models.FloatField()
    organization_unfruitful_contacts_daily = models.FloatField()
    organization_unfruitful_contacts_hourly = models.FloatField()

    organization_unfruitful_costs_monthly = models.FloatField()
    organization_unfruitful_costs_daily = models.FloatField()
    organization_unfruitful_costs_hourly = models.FloatField()

    # lead conversion rates 
    Organization_Lead_Generation_Rate_daily = models.FloatField()
    Organization_Lead_Generation_Rate_hourly = models.FloatField()

    # ABDD Conversion Rates
    ABDD_Lead_Generation_Rate = models.FloatField()
    Organization_Avg_Cost_Per_Lead = models.FloatField()
    ABDD_Avg_Cost_Per_Lead = models.FloatField()
    CPL_Reduction = models.FloatField()

    # sell generation rates
    Organization_Sell_Generation_Rate = models.FloatField()

    # sell generation costs
    Avg_Organization_BDR_Cost_to_Generate_Sale=models.FloatField()
    Avg_ABDD_Cost_to_Generate_Sale=models.FloatField()

    # seller informatiom
    seller_name = models.CharField(max_length=200, default='seller')
    company = models.CharField(max_length=200, default='test')
    
    def __str__(self):
        return self.company
