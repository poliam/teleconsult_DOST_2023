from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('', views.AppointmentList, name="AppointmentList"),
   path('create_appointment', views.CreateAppointment, name="CreateAppointment"),
   path('remove_appointment', views.RemoveAppointment, name="RemoveAppointment"),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)