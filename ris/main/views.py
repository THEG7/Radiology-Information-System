from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from main.forms import AuthUserForm, UserProfileForm, PersonForm, RadiologyRecordForm, UploadImageForm
from main.models import User, Person, RadiologyRecord, PacsImage, FamilyDoctor

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

# Create your views here.

# adapted from http://www.tangowithdjango.com/book/chapters/login.html
def register(request):
    context = RequestContext(request)

    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        auth_user_form = AuthUserForm(data=request.POST)
        user_form = UserProfileForm(data=request.POST)
        person_form = PersonForm(data=request.POST)

        if  auth_user_form.is_valid() and person_form.is_valid() and user_form.is_valid():
            auth_user = auth_user_form.save()

            auth_user.set_password(auth_user.password)
            auth_user.save()

            person = Person.objects.create(**person_form.cleaned_data)
            class_field = user_form.cleaned_data['class_field']

            user = User.objects.create(
                auth_user=auth_user,
                person=person,
                password=auth_user.password,
                username=auth_user.username,
                class_field=class_field)

            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Update our variable to tell the template registration was successful.
            registered = True

        else:
            print auth_user_form.errors, user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        auth_user_form = AuthUserForm()
        person_form = PersonForm()
        user_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'main/registration.html',
            {'user_form': user_form, 'auth_user_form': auth_user_form, 'person_form': person_form, 'registered': registered},
            context)


def user_login(request):
    context = RequestContext(request)
    logged_in = request.user.is_authenticated()
    if logged_in:
        return HttpResponseRedirect('/ris/')

    if request.method == 'POST':
        auth_form = AuthenticationForm(data=request.POST)

        # Use Django's machinery to attempt to see if the username/password
        if auth_form.is_valid():
            user = auth_form.get_user()
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ris/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details"
            print auth_form.errors

    else:
        auth_form = AuthenticationForm()
    return render_to_response('main/login.html', {'auth_form':auth_form}, context)



@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/ris/')



class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context

def create_radiology_record(request):
    # template_name = 'main/create_record.html'

    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        rr_form = RadiologyRecordForm(data=request.POST)
        image_form = UploadImageForm(request.POST,request.FILES)
        if  rr_form.is_valid() and image_form.is_valid():

            patient = Person.objects.get(id=rr_form.cleaned_data['patient'])
            doctor = Person.objects.get(id=rr_form.cleaned_data['doctor'])
            radiologist = Person.objects.get(id=rr_form.cleaned_data['radiologist'])


            radiology_record = RadiologyRecord.objects.create(
                patient=patient,
                doctor=doctor,
                radiologist=radiologist,
                test_type = rr_form.cleaned_data['test_type'],
                prescribing_date = rr_form.cleaned_data['prescribing_date'],
                test_date = rr_form.cleaned_data['test_date'],
                diagnosis = rr_form.cleaned_data['diagnosis'],
                description = rr_form.cleaned_data['description'])

            # image = image_form.cleaned_data['image']
            # path = default_storage.save('temp_img.txt', ContentFile(image.read()))
            image_b64 = base64.b64encode(image_form.cleaned_data['image'].read())
            print image_b64
            pacs_image = PacsImage.objects.create(
                record=radiology_record,
                full_size=image_b64)
            return HttpResponseRedirect('/ris/')

        else:
            print rr_form.errors, image_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        rr_form = RadiologyRecordForm()
        image_form = UploadImageForm()


    # Render the template depending on the context.
    return render_to_response(
            'main/create_record.html',
            {'rr_form': rr_form, 'image_form': image_form},
            context)
