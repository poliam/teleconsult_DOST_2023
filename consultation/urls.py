from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('create/<patient_id>', views.CreateConsultation, name="CreateConsultation"),
   path('details', views.EncounterDetails, name="EncounterDetails"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)