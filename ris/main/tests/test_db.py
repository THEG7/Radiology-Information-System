from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Person, User, FamilyDoctor, PacsImage, RadiologyRecord
from django.contrib.auth.models import User as AuthUser

class DatabaseTestCase(TestCase):
    """
    Basic testing of the model creation and database insertion
    """
    def setUp(self):
        self.doctor = {
            'first_name':'DOCTOR',
            'last_name':'DOCTOR',
            'address':'ADDRESS',
            'email':'doctor@test.com',
            'phone': '+17801234567' }
        self.patient = {
            'first_name':'PATIENT',
            'last_name':'PATIENT',
            'address':'ADDRESS',
            'email':'patient@test.com',
            'phone': '+17801234567' }

    def tearDown(self):
        """Remove all created objects from database"""
        Person.objects.all().delete()
        # User.objects.all().delete()
        # FamilyDoctor.objects.all().delete()
        # PacsImage.objects.all().delete()
        # RadiologyRecord.objects.all().delete()

    def test_set_up(self):
        """ Assert that that the user model is created """
        patient = Person.objects.create(
            first_name=self.patient['first_name'],
            last_name=self.patient['last_name'],
            address=self.patient['address'],
            email=self.patient['email'],
            phone=self.patient['phone'])

        self.assertEquals(patient.first_name, self.patient['first_name'])
        self.assertEquals(patient.last_name, self.patient['last_name'])
        self.assertEquals(patient.email, self.patient['email'])

    def test_create_user(self):
        patient = Person.objects.create(
            first_name=self.patient['first_name'],
            last_name=self.patient['last_name'],
            address=self.patient['address'],
            email=self.patient['email'],
            phone=self.patient['phone'])

        auth_user = AuthUser.objects.create(
            username='username',
            password='password'
        )
        user = User.objects.create(
            auth_user = auth_user,
            person = patient,
            username = auth_user.username,
            password = auth_user.password,
            class_field = 'p'
        )

        #retrieve models
        self.assertEquals((User.objects.get(username=user.username)).username, user.username)
        self.assertEquals((AuthUser.objects.get(id=auth_user.id)).id, auth_user.id)
        self.assertEquals((Person.objects.get(id=patient.id)).id, patient.id)
