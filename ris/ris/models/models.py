from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from ..validators import validate_class_field
from django.core import validators

from uuidfield import UUIDField
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# note: insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.

class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=24, blank=True)
    last_name = models.CharField(max_length=24, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.CharField(unique=True, max_length=128, blank=True)
    phone = models.CharField(max_length=10, blank=True)

    class Meta:
        managed = False
        db_table = 'persons'

class FamilyDoctor(models.Model):
    doctor = models.ForeignKey('Person')
    patient = models.ForeignKey('Person')

    class Meta:
        managed = False
        db_table = 'family_doctor'


class PacsImage(models.Model):
    record = models.ForeignKey('RadiologyRecord')
    image_id = models.IntegerField(primary_key=True)
    thumbnail = models.TextField(blank=True)
    regular_size = models.TextField(blank=True)
    full_size = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'pacs_images'

class RadiologyRecord(models.Model):
    record_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Person, blank=True, null=True)
    doctor = models.ForeignKey(Person, blank=True, null=True)
    radiologist = models.ForeignKey(Person, blank=True, null=True)
    test_type = models.CharField(max_length=24, blank=True)
    prescribing_date = models.DateField(blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    diagnosis = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        managed = False
        db_table = 'radiology_record'


class UserManager(BaseUserManager):

  def _create_user(self, username, person, password, class_field, is_superuser, **extra_fields):
    now = timezone.now()
    today = datetime.date.today

    if not username:
      raise ValueError(_('The given username must be set'))
    user = self.model(user_name=username, person=person,
             class_field=class_field, is_active=True,
             is_superuser=is_superuser, last_login=now,
             date_joined=today, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_user(self, username, person, password=None, class_field='p', **extra_fields):
    return self._create_user(username, person, password, False,
                 **extra_fields)

  def create_superuser(self, username, person, password, class_field='a', **extra_fields):
    user=self._create_user(username, person, password, class_field, True,
                 **extra_fields)
    user.is_active=True
    user.save()
    return user

class User(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(_('username'), primary_key=True, max_length=24,
        help_text=_('Required. 24 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_registered = models.DateField(_('date registered'), blank=True, null=True, default=datetime.date.today)

    person = models.ForeignKey(Person, blank=True, null=True)

    # administrator,patient,doctor,radiologist
    class_field = models.CharField(db_column='class', max_length=1, blank=True,
        validators=[validate_class_field])  # Field renamed because it was a Python reserved word.

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['person']

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.person.first_name, self.person.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.person.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.person.email], **kwargs)
