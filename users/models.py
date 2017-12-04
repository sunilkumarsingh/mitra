# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import os

# Create your models here.
solution_options = (
        ('home', 'Home'),
        ('society', 'Society'),
        ('industry', 'industry'),
    )

def image_upload_path(instance, filename):
    return os.path.basename(filename)

class UserType(models.Model):
    user_type = models.CharField(unique=True, max_length=64, blank=True, null=True)
    is_active = models.BooleanField(default=1)
    created_by = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=64, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pm_user_type'

        def __str__(self):
            return self.name


class User(AbstractUser):
    user_type = models.ForeignKey('UserType',on_delete=models.DO_NOTHING, blank=True, null=True)
    phone_regex = RegexValidator(regex='/^(\+\d{1,3}[- ]?)?\d{10}$/',
                                 message="Mobile number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    mobile = models.CharField(max_length=10, validators=[phone_regex])
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    rooftop_area = models.PositiveIntegerField(blank=True, null=True)
    consumption = models.PositiveIntegerField(blank=True, null=True)
    total_bill_with_taxes = models.PositiveIntegerField(blank=True, null=True)
    total_unit_consumption = models.PositiveIntegerField(blank=True, null=True)
    total_per_unit_cost = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    willing_price_per_unit = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    price_escalation_per_year = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    plant_size_per_RT_area = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    plant_size_per_consumption = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    feasible_in_house_plant = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    customer_profile = models.CharField(max_length=200, blank=True, null=True)
    income = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    cibil_report = models.CharField(max_length=200, blank=True, null=True)
    review = models.CharField(max_length=200, blank=True, null=True)
    min_amount_to_invest = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    max_amount_to_invest = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    IRR_value = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    financial_document_upload = models.FileField(upload_to=image_upload_path, blank=True, null=True)
    created_by = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=64, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pm_user'


class EPC_Details(models.Model):
    user = models.ForeignKey('User',on_delete=models.DO_NOTHING)
    solution_provider = models.CharField(max_length=64, blank=True, null=True)
    registered_name = models.CharField(max_length=64, blank=True, null=True)
    epc_profile = models.CharField(max_length=64, blank=True, null=True)
    about_epc = models.CharField(max_length=200, blank=True, null=True)
    years_of_experience = models.CharField(max_length=10, blank=True, null=True)
    projects_in_india = models.PositiveIntegerField(blank=True, null=True)
    projects_outside_india = models.PositiveIntegerField(blank=True, null=True)
    executed_projects = models.PositiveIntegerField(blank=True, null=True)
    ongoing_projects = models.PositiveIntegerField(blank=True, null=True)
    references_to_verify = models.CharField(max_length=64, blank=True, null=True)
    cost_quality_rate = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    # rooftop_area = models.PositiveIntegerField(blank=True, null=True) Integer
    annual_demand = models.PositiveIntegerField(blank=True, null=True)
    bid_for_building_plant = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    feasible_in_house_plant = models.CharField(max_length=64, blank=True, null=True)
    module_manufacturer = models.CharField(max_length=64, blank=True, null=True)
    inverter_manufacturer = models.CharField(max_length=64, blank=True, null=True)
    wiring_cost_range = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    civil_work_range = models.CharField(max_length=64, blank=True, null=True)
    labor = models.CharField(max_length=64, blank=True, null=True)
    total_cost_range = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    review = models.CharField(max_length=200, blank=True, null=True)
    sme_range = models.CharField(max_length=64, blank=True, null=True)
    cibil = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'pm_epc_details'


class Solar_Estimator(models.Model):
    user = models.ForeignKey('User',on_delete=models.DO_NOTHING)
    roof_toparea_info = models.CharField(max_length=64, blank=True, null=True)
    solution_for = models.CharField(max_length=20, choices=solution_options)
    consumption_per_month = models.CharField(max_length=64, blank=True, null=True)
    avg_bill_per_month = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    pin = models.PositiveIntegerField(blank=True, null=True)
    phone_regex = RegexValidator(regex='/^(\+\d{1,3}[- ]?)?\d{10}$/',
                                 message="Mobile number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    mobile = models.CharField(max_length=10, validators=[phone_regex], blank=True)
    created_by = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=64, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pm_solar_estimator'


class ProjectStatus(models.Model):
    status = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by =  models.CharField(max_length=64, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by =  models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = "ebc_project_status"
        ordering = ['-pk']

    def __unicode__(self):
        return self.status


class Project_Details(models.Model):
    customer = models.ForeignKey('User',on_delete=models.DO_NOTHING, related_name='project_customer')
    investor = models.ForeignKey('User',on_delete=models.DO_NOTHING, related_name='project_investor')
    epc = models.ForeignKey('User',on_delete=models.DO_NOTHING, related_name='project_epc')
    epc_Details = models.CharField(max_length=200, blank=True, null=True)
    payment_details = models.CharField(max_length=64, blank=True, null=True)
    units_generated = models.PositiveIntegerField(blank=True, null=True)
    amount_due = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    next_payment_date = models.DateTimeField(blank=True, null=True)
    next_payment_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    status = models.ForeignKey('ProjectStatus',on_delete=models.DO_NOTHING)
    no_of_units_generated = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    Revnue = models.PositiveIntegerField(blank=True, null=True)
    operation_and_maintainance = models.PositiveIntegerField(blank=True, null=True)
    battery_replacement_cost = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    miscellaneous = models.CharField(max_length=200, blank=True, null=True)
    commission_cost =models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by =  models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = "ebc_project_details"
        ordering = ['-pk']


class Basic_Assumptions(models.Model):
    discounting_factor = models.PositiveIntegerField(blank=True, null=True)
    tax_benefits_for_no_of_years = models.PositiveIntegerField(blank=True, null=True)
    accelerated_depreciation = models.CharField(max_length=64, blank=True, null=True)
    area_required_for_1KW_plant_sqft = models.PositiveIntegerField(blank=True, null=True)
    electricity_generated_per_annum_per_kw = models.PositiveIntegerField(blank=True, null=True)
    cost_of_plant_including_batteries_for_1kw = models.PositiveIntegerField(blank=True, null=True)
    cost_of_plant_without_batteries_for_1kw = models.PositiveIntegerField(blank=True, null=True)
    decrease_in_plant_output_1styear = models.PositiveIntegerField(blank=True, null=True)
    decrease_in_plant_output_everyyear_after_1styear = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = "ebc_basic_assumptions"
        ordering = ['-pk']