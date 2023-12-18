from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from patient.models import details, relatives, medicine, allergies
from consultation.models import *
from consultation.consultation_form import AddConsultationEncounterForm
import random, os
from datetime import date, datetime, timedelta

# Create your views here.
@login_required(login_url='/login')
def AppointmentList(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Admin"

	print(returnVal['group_type'])
	returnVal['sidebar'] = "appointment"
	returnVal['userDetails'] = profile_details
	current_date = date.today()
	future_date = current_date + timedelta(days=7)
	returnVal['week_consultation'] = encounter.objects.filter(consultation_date__range=(current_date, future_date)).order_by('consultation_date')
	current_date_split = str(current_date).split("-")
	this_month = current_date_split[1]
	returnVal['month_consultation'] = encounter.objects.filter(consultation_date__month=this_month).order_by('consultation_date')
	past_dates = current_date-timedelta(hours=24)
	returnVal['past_consultation'] = encounter.objects.filter(consultation_date__lte=past_dates).order_by('consultation_date')
	returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0)
	returnVal['consultationEncounterForm'] = AddConsultationEncounterForm()

	if request.method == 'POST':
		consultationEncounterForm = AddConsultationEncounterForm(request.POST)
		returnVal['consultationEncounterForm'] = consultationEncounterForm
		patient_id = request.POST['patient_id']
		try:
			patient_instance = details.objects.get(pk=patient_id)
		except:
			returnVal['error_msg'] = "Patient Does not exists"
			return render(request, "appointment_dashboard.html", returnVal)

		if consultationEncounterForm.is_valid():
			EncounterPost = consultationEncounterForm.save(commit=False)
			EncounterPost.details = patient_instance
			EncounterPost.save()

	return render(request, "appointment_dashboard.html", returnVal)

@login_required(login_url='/login')
def CreateAppointment(request):
	return redirect("AppointmentList")