from django.contrib import admin

from people.models import Person, Marriage, Residence, ResidenceTenant, Action

admin.site.register(Marriage)
admin.site.register(Residence)
admin.site.register(ResidenceTenant)
admin.site.register(Person)
admin.site.register(Action)
