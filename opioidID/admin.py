from django.contrib import admin
from .models import *
# Register your models here.

class CredentialTabularInline(admin.TabularInline):
    model = Credential
    list_display = ["credential"]
    extra = 0

class PrescriberAdmin(admin.ModelAdmin):
    inlines = [CredentialTabularInline]

admin.site.register(Prescriber, PrescriberAdmin)
admin.site.register(Drug)
admin.site.register(DrugPrescriber)
admin.site.register(Credential)
admin.site.register(State)