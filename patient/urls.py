from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('patient', views.PatientLists, name="PatientLists"),
   path('patient_create', views.PatientCreate, name="PatientCreate"),
   path('patient_detailed/<patient_id>', views.PatientDetailed, name="PatientDetailed"),
   path('patient_edit/<patient_id>', views.PatientEdit, name="PatientEdit"),
   path('patient_create_relative/<patient_id>', views.PatientCreateRelative, name="PatientCreateRelative"),
   path('patient_edit_relative/<relative_id>', views.PatientEditRelative, name="PatientEditRelative"),
   path('patient_create_allergy/<patient_id>', views.PatientCreateAllergy, name="PatientCreateAllergy"),
   path('patient_create_gps/<patient_id>', views.PatientCreateGPS, name="PatientCreateGPS"),
   path('patient_update_gps/<gps_id>', views.PatientUpdateGPS, name="PatientUpdateGPS"),
   path('patient_create_hamd/<patient_id>', views.PatientCreateHamD, name="PatientCreateHamD"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)