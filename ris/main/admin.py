from django.contrib import admin

from main.models import Person, User, FamilyDoctor, PacsImage, RadiologyRecord
from django.contrib.auth.models import User as AuthUser
from daterange_filter.filter import DateRangeFilter
# Model options
class PersonOptions(admin.ModelAdmin):
    readonly_fields = ('id',)


class UserOptions(admin.ModelAdmin):

    list_display = ['class_field', 'auth_user', 'person', 'date_registered']
    list_editable = ['class_field', 'auth_user', 'person', 'date_registered']
    list_filter = ('class_field', ('date_registered', DateRangeFilter))


class PacsImageOptions(admin.TabularInline):
    model = PacsImage

class RadiologyRecordOptions(admin.ModelAdmin):
    list_display = [
        'get_first_name',
        'get_last_name',
        'get_address',
        'get_email',
        'get_phone',
        'test_date',
        'diagnosis'
    ]
    inlines = [
            PacsImageOptions,
    ]
    list_filter = (
        'diagnosis',
        ('test_date', DateRangeFilter),
        ('prescribing_date', DateRangeFilter)
    )

    search_fields = [
        'patient__first_name',
        'patient__last_name',
        'radiologist__first_name',
        'radiologist__last_name',
        'doctor__first_name',
        'doctor__last_name',
        'diagnosis',
        'description']

    def get_first_name(self, obj):
        return obj.patient.first_name
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'patient__first_name'

    def get_last_name(self, obj):
        return obj.patient.last_name
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'patient__last_name'

    def get_address(self, obj):
        return obj.patient.address
    get_address.short_description = 'Address'
    get_address.admin_order_field = 'patient__address'

    def get_email(self, obj):
        return obj.patient.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'patient__email'

    def get_phone(self, obj):
        return obj.patient.phone
    get_phone.short_description = 'Phone Number'
    get_phone.admin_order_field = 'patient__phone'


# Register your models here.
admin.site.register(Person, PersonOptions)
admin.site.register(User, UserOptions)
admin.site.register(FamilyDoctor)
admin.site.register(PacsImage)
admin.site.register(RadiologyRecord, RadiologyRecordOptions)
