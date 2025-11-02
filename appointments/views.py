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
from consultation.consultation_form import AddConsultationEncounterForm, AddPsychiatricEvaluateForm
import random, os
from datetime import date, datetime, timedelta

# Create your views here.
@login_required(login_url='/login')
def AppointmentList(request):
    returnVal = {}

    # Get the logged-in user's group and set the workplace_choice accordingly
    if request.user.groups.filter(name="Doctor").exists():
        returnVal['group_type'] = "Doctor"
        workplace_choice = None  # No specific workplace for Doctor
    elif request.user.groups.filter(name="Nurse-R").exists():
        returnVal['group_type'] = "Nurse"
        workplace_choice = 'Riyadh'
    elif request.user.groups.filter(name="Nurse-J").exists():
        returnVal['group_type'] = "Nurse"
        workplace_choice = 'Jeddah'
    elif request.user.groups.filter(name="Triage").exists():
        returnVal['group_type'] = "Triage"
        workplace_choice = None  # No specific workplace for Triage
    elif request.user.groups.filter(name="Admin").exists():
        returnVal['group_type'] = "Admin"
        workplace_choice = None  # Admin can access all workplaces

    # Default value for workplace_choice if not defined above
    if 'workplace_choice' not in locals():
        workplace_choice = None

    # Sidebar and user details
    returnVal['sidebar'] = "appointment"
    profile_details = User.objects.get(pk=request.user.id)  # Get the profile details of the logged-in user
    returnVal['userDetails'] = profile_details

    # Get the current date and calculate future date (7 days from today)
    current_date = date.today()
    future_date = current_date + timedelta(days=7)

    # Filter consultations based on workplace choice
    if workplace_choice:
        returnVal['week_consultation'] = encounter.objects.filter(consultation_date__range=(current_date, future_date), is_delete=0, details__workplace=workplace_choice).order_by('consultation_date')
        returnVal['month_consultation'] = encounter.objects.filter(consultation_date__year=current_date.year, consultation_date__month=current_date.month, is_delete=0).order_by('consultation_date')
        returnVal['past_consultation'] = encounter.objects.filter(consultation_date__lte=current_date - timedelta(hours=24), is_delete=0, details__workplace=workplace_choice).order_by('consultation_date')
        returnVal['list_of_psychiatric_evaluate'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date__range=(current_date, future_date), is_delete=0, details__workplace=workplace_choice).order_by('evaluation_consultation_date')
        returnVal['list_of_psychiatric_evaluate_month'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date__year=current_date.year, evaluation_consultation_date__month=current_date.month, is_delete=0, details__workplace=workplace_choice).order_by('evaluation_consultation_date')
        returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0, workplace=workplace_choice)
    else:
        # If no specific workplace is assigned (e.g., Doctor, Admin)
        returnVal['week_consultation'] = encounter.objects.filter(consultation_date__range=(current_date, future_date), is_delete=0).order_by('consultation_date')
        returnVal['month_consultation'] = encounter.objects.filter(consultation_date__year=current_date.year, consultation_date__month=current_date.month, is_delete=0).order_by('consultation_date')
        returnVal['past_consultation'] = encounter.objects.filter(consultation_date__lte=current_date - timedelta(hours=24), is_delete=0).order_by('consultation_date')
        returnVal['list_of_psychiatric_evaluate'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date__range=(current_date, future_date), is_delete=0).order_by('evaluation_consultation_date')
        returnVal['list_of_psychiatric_evaluate_month'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date__month=current_date.month, evaluation_consultation_date__year=current_date.year, is_delete=0).order_by('evaluation_consultation_date')
        returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0)

    # Process the form for adding a consultation or psychiatric evaluation
    returnVal['consultationEncounterForm'] = AddConsultationEncounterForm()
    returnVal['PsychiatricEvaluateForm'] = AddPsychiatricEvaluateForm()

    if request.method == 'POST':
        consultationEncounterForm = AddConsultationEncounterForm(request.POST)
        returnVal['consultationEncounterForm'] = consultationEncounterForm
        PsychiatricEvaluateForm = AddPsychiatricEvaluateForm(request.POST)
        returnVal['PsychiatricEvaluateForm'] = PsychiatricEvaluateForm
        patient_id = request.POST['patient_id']
        try:
            patient_instance = details.objects.get(pk=patient_id)
        except:
            returnVal['error_msg'] = "Patient Does not exist"
            return render(request, "appointment_dashboard.html", returnVal)

        if request.POST['consultation_type'] == "consultation":
            if consultationEncounterForm.is_valid():
                EncounterPost = consultationEncounterForm.save(commit=False)
                EncounterPost.details = patient_instance
                EncounterPost.save()
        else:
            if PsychiatricEvaluateForm.is_valid():
                PsychiatricEvaluatePost = PsychiatricEvaluateForm.save(commit=False)
                PsychiatricEvaluatePost.details = patient_instance
                PsychiatricEvaluatePost.create_by = request.user
                PsychiatricEvaluatePost.save()
        return redirect("CreateAppointment")
    return render(request, "appointment_dashboard.html", returnVal)

@login_required(login_url='/login')
def CreateAppointment(request):
	return redirect("AppointmentList")

@login_required(login_url='/login')
def RemoveAppointment(request):
	if request.method == 'POST':
		if request.POST.get('dataType') == "PsychiatryEvaluation":
			data_id = request.POST.get('dataTypeID')

			instanceDetails = get_object_or_404(psychiatric_evaluate, id=data_id)
			instanceDetails.is_delete = 1
			instanceDetails.save()
		elif request.POST.get('dataType') == "Consultation":
			data_id = request.POST.get('dataTypeID')
			instanceDetails = get_object_or_404(encounter, id=data_id)
			instanceDetails.is_delete = 1
			instanceDetails.save()

	return redirect("AppointmentList")
