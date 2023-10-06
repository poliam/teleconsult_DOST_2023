from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('patient', views.PatientLists, name="PatientLists"),
   path('patient_create', views.PatientCreate, name="PatientCreate"),
   path('patient_detailed/<patient_id>', views.PatientDetailed, name="PatientDetailed"),
   path('patient_edit/<patient_id>', views.PatientEdit, name="PatientEdit")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)