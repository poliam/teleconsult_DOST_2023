from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from patient.models import details, relatives, medicine, allergies
from consultation.models import *
import random, os
from datetime import date, datetime

@login_required(login_url='/login')
def CreateConsultation(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "Consultation"
	returnVal['userDetails'] = profile_details
	returnVal['grooming_list'] = dress_and_grooming.objects.all()
	returnVal['attitude_list'] = attitude.objects.all()
	returnVal['facialexpression_list'] = facialexpression.objects.all()
	returnVal['movement_list'] = movement.objects.all()
	returnVal['motoactive_list'] = motoactive.objects.all()
	returnVal['speech_list'] = speech.objects.all()
	returnVal['aphasia_list'] = aphasia.objects.all()
	returnVal['mood_list'] = mood.objects.all()
	returnVal['affect_list'] = affect.objects.all()
	returnVal['insomnia_list'] = insomnia.objects.all()
	returnVal['orientation_list'] = orientation.objects.all()
	returnVal['memory_list'] = memory.objects.all()
	returnVal['disorderedperception_list'] = disorderedperception.objects.all()
	returnVal['thoughtcontent_list'] = thoughtcontent.objects.all()
	returnVal['delusioncontent_list'] = delusioncontent.objects.all()
	returnVal['thoughtform_list'] = thoughtform.objects.all()
	returnVal['preoccupation_list'] = preoccupation.objects.all()
	returnVal['condition_list'] = condition.objects.all()
	try:
		patient_detailed = details.objects.get(pk=patient_id)
	except:
		returnVal['error_msg'] = "Patient Does not exists"
		return render(request, 'consultation_create.html', returnVal)

	returnVal['patientDetailed'] = patient_detailed
	return render(request, 'consultation_create.html', returnVal)
# Create your views here.
