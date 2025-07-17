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
   path('patient_remove_relative', views.PatientRemoveRelative, name="PatientRemoveRelative"),
   path('patient_get_relative', views.PatientGetRelative, name="PatientGetRelative"),


   path('patient_create_allergy/<patient_id>', views.PatientCreateAllergy, name="PatientCreateAllergy"),
   path('patient_delete_allergy', views.PatientDeleteAllergy, name="PatientDeleteAllergy"),

   path('patient_create_gps/<patient_id>', views.PatientCreateGPS, name="PatientCreateGPS"),
   path('patient_update_gps/<gps_id>', views.PatientUpdateGPS, name="PatientUpdateGPS"),
   path('patient_get_gps', views.PatientGetGPS, name="PatientGetGPS"),
   path('patient_autosave_gps', views.PatientAutoSaveGPS, name="PatientAutoSaveGPS"),
   path('patient_delete_gps/<int:gps_id>/', views.PatientDeleteGPS, name="PatientDeleteGPS"),

   path('patient_create_hamd/<patient_id>', views.PatientCreateHamD, name="PatientCreateHamD"),
   path('patient_update_hamd/<hamd_id>', views.PatientUpdateHamD, name="PatientUpdateHamD"),
   path('patient_get_hamd', views.PatientGetHamd, name="PatientGetHamd"),
   path('patient_autosave_hamd', views.PatientAutoSaveHamd, name="PatientAutoSaveHamd"),
   path('patient_delete_hamd/<int:hamd_id>/', views.PatientDeleteHamD, name="PatientDeleteHamD"),

   path('patient_survey/<patient_id>', views.PatientSurvey, name="PatientSurvey"),
   path('patient_view_survey/<patient_id>', views.PatientViewSurvey, name="PatientViewSurvey"),
   path('survey_completed', views.PatientSurveyCompleted, name="PatientSurveyCompleted"),

   path('patient_file_upload', views.PatientFileUpload, name="PatientFileUpload"),
   path('patient_referral_pdf/<int:referral_id>/', views.referralFormPdf, name='referralFormPdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)