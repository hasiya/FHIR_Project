from django.contrib import admin
from .models import Patient, Encounter, Condition, ExplanationOfBenefit

# Register your models here.
admin.site.register(Patient)
admin.site.register(Encounter)
admin.site.register(Condition)
admin.site.register(ExplanationOfBenefit)
