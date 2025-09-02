from django.contrib import admin
from .models import User, Patient, Doctor, PatientDoctorMapping

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)
