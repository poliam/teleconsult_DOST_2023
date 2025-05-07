"""
URL configuration for Teleconsult project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views as TeleconsultView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TeleconsultView.dashboard, name="dashboard"),
    path("login", TeleconsultView.login_user, name="login_user"),
    path('logout', TeleconsultView.Logout, name="Logout"),
    path('signup', TeleconsultView.signup, name="signup"),
    path('change-password/', TeleconsultView.change_password, name='change-password'),
    path('reports/', TeleconsultView.reportPage, name='reports'),
    path('reports/charts', TeleconsultView.reportCharts, name='reportCharts'),
    path('reports/tables', TeleconsultView.reportTables, name="reportTables"),
    path('download/<file_id>/', TeleconsultView.download_file, name='download_file'),
    path('patient/', include('patient.urls')),
    path('consultation', include('consultation.urls')),
    path('appointment/', include('appointments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
