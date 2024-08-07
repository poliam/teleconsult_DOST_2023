from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('create/<patient_id>', views.CreateConsultation, name="CreateConsultation"),
   path('edit/<encounter_id>', views.EditConsultation, name='EditConsultation'),
   path('details', views.EncounterDetails, name="EncounterDetails"),

   path('create_HOPI', views.CreateHOPI, name="CreateHOPI"),
   path('delete_HOPI', views.DeleteHOPI, name="DeleteHOPI"),
   path('auto_create_HOPI', views.AutoCreateHOPI, name="AutoCreateHOPI"),

   path('create_diagnosis', views.CreateDiagnosis, name="CreateDiagnosis"),
   path('delete_diagnosis', views.DeleteDiagnosis, name="DeleteDiagnosis"),

   path('create_treatment', views.CreateTreatment, name="CreateTreatment"),
   path('delete_treatment', views.DeleteTreatment, name="DeleteTreatment"),

   path('create_nurse_notes', views.CreateNurseNotes, name="CreateNurseNotes"),
   path('get_nurse_notes', views.getNurseList, name="getNurseList"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)