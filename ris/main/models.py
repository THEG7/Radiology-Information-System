from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
import datetime


class Person(models.Model):
    id = models.AutoField(primary_key=True, db_column="person_id")
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(unique=True, max_length=128)
    phone = models.CharField(max_length=14, null=True, blank=True)

    class Meta:
        # managed = False
        db_table = 'persons'

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s (id=%s)' % (self.full_name, self.id)



class User(models.Model):
    CLASS_CHOICES = (
        ('a', 'administrator'),
        ('p', 'patient'),
        ('d', 'doctor'),
        ('r', 'radiologist'),
    )
    auth_user = models.OneToOneField(AuthUser, null=True)
    username = models.CharField(primary_key=True, max_length=24, db_column="user_name")
    password = models.CharField(max_length=128, blank=True)
    class_field = models.CharField(db_column='class', max_length=1, choices=CLASS_CHOICES, blank=True, default='p')  # Field renamed because it was a Python reserved word.
    person = models.ForeignKey(Person, db_column="person_id", null=True)
    date_registered = models.DateField(blank=True, null=True, default=datetime.date.today)

    class Meta:
        # managed = False
        db_table = 'users'

    def __unicode__(self):
        return u'%s' % self.username



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
    thumbnail = models.TextField(null=True, blank=True)
    regular_size = models.TextField(null=True, blank=True)
    full_size = models.TextField(null=True, blank=True)

    class Meta:
        # managed = False
        db_table = 'pacs_images'

    def __unicode__(self):
        return u'%s' % self.image_id



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

    def __unicode__(self):
        return u'%s' % self.record_id
