from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Person, User, FamilyDoctor, PacsImage, RadiologyRecord

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
    #
    # def test_create_user(self):
    #     try:
    #         person = Person.objects.create(user = self.user,
    #             github_username = GITHUB_USERNAME,
    #             bio = BIO)
    #     except:
    #         self.assertFalse(True, 'Author object not created and inserted into db')
    #
    # def test_author_delete_by_id(self):
    #     author = Author.objects.create(user = self.user)
    #     try:
    #         query = Author.objects.filter(id = author.id).delete()
    #         self.assertEquals(query, None)
    #     except:
    #         self.assertFalse(True, 'Author deletion failed')
