from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    full_name = models.CharField(max_length=500)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def __str__(self):
        return self.email


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_mail = models.EmailField(default='test@gmail.com')
    lead_full_name = models.CharField(max_length=230)
    lead_full_name_possesive = models.CharField(max_length=250)
    lead_interest = models.TextField() 
    lead_social_links = models.TextField()
    lead_experience = models.TextField()
    company_city = models.CharField(max_length=200)
    company_state = models.CharField(max_length=202)
    company_site = models.CharField(max_length=205)
    company = models.CharField(max_length=500)
    lead_skills = models.TextField()
    lead_position = models.CharField(max_length=206)

    def __str__(self):
        return self.lead_full_name


class Business_case_data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.ForeignKey(MyUser, null=False , on_delete=models.CASCADE)
    lead= models.ForeignKey(Lead, null=False , on_delete=models.CASCADE)
    email = models.EmailField(default='test@gmail.com')
    Avg_BDR_Salary = models.FloatField()
    Avg_BDR_Training_Costs = models.FloatField()
    Avg_BDR_Benefits = models.FloatField()
    Annual_Organization_BDR_Costs = models.FloatField()
    Daily_Organization_BDR_Costs = models.FloatField()
    Hourly_Organization_BDR_Costs = models.FloatField()
    Monthly_Organization_BDR_Costs = models.FloatField(default=0)

    # conversion rates
    Contacts_Monthly = models.FloatField(default=0)
    Contacts_Daily = models.FloatField(default=0)
    Contacts_Hourly = models.FloatField(default=0)
    Leads_Monthly = models.FloatField(default=0)
    Contact_to_Lead_Rate = models.FloatField(default=0)
    contacts_to_generate_each_lead = models.FloatField(default=0)
    leads_needed_to_generate_each_sale = models.FloatField(default=0)

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
    ABDD_Lead_Generation_Rate_daily = models.FloatField(default=0)
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

    # accounts needed
    Accounts_needed = models.FloatField( default=0)

    # rev share
    Rev_share = models.FloatField( default=0)

    # speed
    org_abdd_process_ratio = models.FloatField( default=0)
    ind_abdd_process_ratio = models.FloatField( default=0)

    # background sevices
    background_email = models.TextField(default='still procesing email, check back again...')
    prospect_report = models.TextField(default='still procesing prospect report, check back again...')
    background_text = models.TextField(default='still procesing prospect text, check back again...')

    dashboard_link = models.CharField(max_length=300, default='email@email.com')

    
    def __str__(self):
        return self.email
    





