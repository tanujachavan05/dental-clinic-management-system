from django.contrib import admin 
from .models import Patient, Blog, Doctor  # ✅ Import Doctor model also

# ✅ Register Patient model
admin.site.register(Patient)

# ✅ Register Blog model
admin.site.register(Blog)

# ✅ Register Doctor model with customization
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization')
    search_fields = ('first_name', 'last_name', 'specialization')
