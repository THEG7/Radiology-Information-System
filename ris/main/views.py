from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from main.forms import AuthUserForm, UserProfileForm, PersonForm, UploadForm
from main.models import Person, User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

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
