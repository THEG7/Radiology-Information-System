from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    address = models.CharField(max_length=128)
    email = models.CharField(unique=True, max_length=128)
    phone = models.CharField(max_length=16)

    class Meta:
        # managed = False
        db_table = 'persons'


class User(models.Model):
    CLASS_CHOICES = (
        ('a', 'administrator'),
        ('p', 'patient'),
        ('d', 'doctor'),
        ('r', 'radiologist'),
    )
    auth_user = models.OneToOneField(AuthUser, null=True)
    user_name = models.CharField(primary_key=True, max_length=24)
    password = models.CharField(max_length=24, blank=True)
    class_field = models.CharField(db_column='class', max_length=1, blank=True, choices=CLASS_CHOICES, default='a')  # Field renamed because it was a Python reserved word.
    person = models.ForeignKey(Person, db_column="person_id", null=True)
    date_registered = models.DateField(blank=True, null=True, default=datetime.date.today)

    class Meta:
        # managed = False
        db_table = 'users'


class FamilyDoctor(models.Model):
    doctor = models.ForeignKey(Person, related_name='doctor', db_column="doctor_id", null=True)
    patient = models.ForeignKey(Person, related_name='patient', db_column="patient_id", null=True)

    class Meta:
        # managed = False
        db_table = 'family_doctor'
        unique_together = (("patient", "doctor"),)

class PacsImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    record = models.ForeignKey('RadiologyRecord', db_column="record_id", null=True)
    thumbnail = models.TextField(blank=True)
    regular_size = models.TextField(blank=True)
    full_size = models.TextField(blank=True)

    class Meta:
        # managed = False
        db_table = 'pacs_images'

class RadiologyRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Person, related_name='patient_r', db_column="patient_id", null=True)
    doctor = models.ForeignKey(Person, related_name='doctor_r', db_column="doctor_id", null=True)
    radiologist = models.ForeignKey(Person, related_name='radiologist', db_column="radiologist_id", null=True)
    test_type = models.CharField(max_length=24, blank=True)
    prescribing_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    test_date = models.DateField(blank=True, null=True)
    diagnosis = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        # managed = False
        db_table = 'radiology_record'
