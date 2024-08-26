from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey
from patient.patient_forms import AddRelativesForm, EditRelativesForm, AddPatientForm, AddPatientAddressForm, EditPatientForm, EditPatientAddressForm, patientSurveyForm, patientFilesForm
from consultation.models import encounter
import random, os


from datetime import date, datetime


@login_required(login_url='/login')
def PatientLists(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	list_of_patients = details.objects.filter(is_delete=0)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['list_of_patients'] = list_of_patients
	return render(request, 'patient_list.html', returnVal)

@login_required(login_url='/login')
def PatientCreate(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['error_msg'] = ""
	returnVal['form'] = AddPatientForm()
	returnVal['FormAddPatientAddress'] = AddPatientAddressForm()

	if request.method == 'POST':
		patientform = AddPatientForm(request.POST, request.FILES)
		AddressForm = AddPatientAddressForm(request.POST)
		returnVal['form'] = patientform
		returnVal['FormAddPatientAddress'] = AddressForm
		if patientform.is_valid() and AddressForm.is_valid():
			if patientform.patientCheck():
				returnVal['error_msg'] = patientform.patientCheck()
				return render(request, 'patient_create.html', returnVal)
			else:
				patient_instance = patientform.save()
				if patient_instance:
					AddressFormPost = AddressForm.save(commit=False)
					AddressFormPost.details = patient_instance
					AddressFormPost.save()

					return redirect("PatientDetailed", patient_id=patient_instance.pk)
				else:
					returnVal['error_msg'] = "error on saving patient!"
					return render(request, 'patient_create.html', returnVal)

		else:
			returnVal['error_msg'] = patientform.errors
			return render(request, 'patient_create.html', returnVal)

		
	return render(request, 'patient_create.html', returnVal)



@login_required(login_url='/login')
def PatientEdit(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	patient_instance = details.objects.get(pk=patient_id)
	returnVal['patientDetailed'] = patient_instance
	returnVal['form'] = EditPatientForm(instance=patient_instance)
	try:
		patient_address = address.objects.get(details=patient_instance)
		returnVal['FormEditPatientAddress'] = EditPatientAddressForm(instance=patient_address)
	except:
		returnVal['FormEditPatientAddress'] = EditPatientAddressForm()
	
	if request.method == 'POST':
		patientform = EditPatientForm(request.POST, request.FILES, instance=patient_instance)
		addressForm = EditPatientAddressForm(request.POST, instance=patient_address)
		returnVal['form'] = patientform
		returnVal['FormEditPatientAddress'] = addressForm
		if patientform.is_valid() and addressForm.is_valid():
			patientform.save()
			addressForm.save()
			return redirect("PatientDetailed", patient_id=patient_instance.pk)
		else:
			returnVal['error_msg'] = patientform.errors
			return render(request, 'patient_create.html', returnVal)

	return render(request, 'patient_edit.html', returnVal)

@login_required(login_url='/login')
def PatientDetailed(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	patient_instance = details.objects.get(pk=patient_id)
	returnVal['patientFilesForm'] = patientFilesForm()
	try:
		patient_survey.objects.get(details = patient_instance.pk)
		returnVal['has_survey'] = 1
	except:
		returnVal['has_survey'] = 0 
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	else:
		returnVal['group_type'] = "Admin"

	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['patientDetailed'] = patient_instance
	returnVal['CURRENT_URL'] = settings.CURRENT_URL
	returnVal['age'] = datetime.now().year - 	patient_instance.BOD.year
	returnVal['list_of_relatives'] = relatives.objects.filter(details=patient_id, is_delete=0)
	returnVal['list_of_allergies'] = allergies.objects.filter(details=patient_id, is_delete=0)
	returnVal['list_of_GPS'] = global_psychotrauma_screen.objects.filter(details=patient_id)
	list_of_hamd = hamd.objects.filter(details=patient_id)

	returnVal['list_of_hamd'] = [{"pk": hamd.pk, "consultation_date": hamd.consultation_date, "score": int(hamd.score), "total_score": hamd.total_score} for hamd in list_of_hamd]


	returnVal['list_of_encounter'] = encounter.objects.filter(details=patient_id).order_by('-consultation_date')
	return render(request, 'patient_detailed.html', returnVal)

@login_required(login_url='/login')
def PatientCreateRelative(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"

	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['patient_id'] = patient_id
	
	try:
		patient_instance = details.objects.get(pk=patient_id)
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_create_relative.html', returnVal)
	form = AddRelativesForm()
	returnVal['form'] = form
	if request.method == 'POST':

		RelativesForm = AddRelativesForm(request.POST)
		returnVal['form'] = RelativesForm
		if RelativesForm.is_valid():
			RelativesPost = RelativesForm.save(commit=False)
			RelativesPost.details = patient_instance
			try:
				RelativesPost.save()
				return redirect("PatientDetailed", patient_id=patient_instance.pk)
			except:
				returnVal['error_msg'] = "Error on Saving a Patient relative!"
				return render(request, 'patient_create_relative.html', returnVal)
		else:
			returnVal['error_msg'] = form.errors
			return render(request, 'patient_create_relative.html', returnVal)

	return render(request, 'patient_create_relative.html', returnVal)


@login_required(login_url='/login')
def PatientEditRelative(request, relative_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	
	try:
		relative_details = relatives.objects.get(pk=relative_id)
	except:
		returnVal['error_msg'] = "Relative Does not exists!"
		return render(request, 'patient_edit_relative.html', returnVal)
	form = EditRelativesForm(instance=relative_details)
	returnVal['form'] = form
	if request.method == 'POST':
		form = EditRelativesForm(request.POST, instance=relative_details)
		returnVal['form'] = form
		if form.is_valid():
			form.save()
			return redirect("PatientDetailed", patient_id=relative_details.details.pk)
		else:
			returnVal['error_msg'] = "Error on Saving a Patient relative!"
			return render(request, 'patient_edit_relative.html', returnVal)
	
	returnVal['relative_details'] = relative_details
	return render(request, 'patient_edit_relative.html', returnVal)

@login_required(login_url='/login')
def PatientGetRelative(request):
	returnVal = {}
	returnVal['status_code'] = 0
	relative_id = request.GET['relative_id']
	try:
		relative_details = relatives.objects.get(pk=relative_id)
	except:
		returnVal['error_msg'] = "Relative Does not exists!"
		return JsonResponse(returnVal, safe=False)
	returnVal['relative_name'] = relative_details.last_name+", "+relative_details.first_name+" "+relative_details.middle_name
	returnVal['relative_gender'] = relative_details.gender
	returnVal['relative_gender_indentity'] = relative_details.gender_indentity
	returnVal['relative_age'] = relative_details.age
	returnVal['relative_marital_status'] = relative_details.marital_status
	returnVal['relative_relationship'] = relative_details.relationship
	returnVal['relative_high_education'] = relative_details.high_education
	returnVal['relative_occupation'] = relative_details.occupation
	returnVal['relative_Workplace'] = relative_details.Workplace
	returnVal['relative_contact_number'] = relative_details.contact_number
	returnVal['relative_email'] = relative_details.email
	returnVal['relative_is_emergency'] = relative_details.is_emergency
	returnVal['status_code'] = 1
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='/login')
def PatientCreateAllergy(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['medicine'] = medicine.objects.filter(is_delete=0, status=1)
	try:
		patient_instance = details.objects.get(pk=patient_id)
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_create_allergies.html', returnVal)
	returnVal['patientDetailed'] = patient_instance

	if request.method == "POST":
		medicine_name = request.POST['medicine_name']
		try:
			medicine_instance = medicine.objects.get(name=medicine_name)
		except:
			new_medicine = medicine()
			new_medicine.name = medicine_name
			try:
				new_medicine.save()
			except:
				returnVal['error_msg'] = "Error on creating medicine"
				return render(request, 'patient_create_allergies.html', returnVal)
			medicine_instance = new_medicine
		new_allergy = allergies()
		new_allergy.medicine_name = medicine_instance
		new_allergy.details = patient_instance
		try:
			new_allergy.save()
			return redirect("PatientDetailed", patient_id=patient_instance.pk)
		except:
			returnVal['error_msg'] = "Error on saving allergies"
			return render(request, 'patient_create_allergies.html', returnVal)
	return render(request, 'patient_create_allergies.html', returnVal)

@login_required(login_url='/login')
def PatientCreateGPS(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['patientId'] = patient_id
	try:
		patient_instance = details.objects.get(pk=patient_id)
		returnVal['patientDetail'] = patient_instance
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_create_gps.html', returnVal)

	if request.method == "POST":
		gps_instance = Create_global_psychotrauma_screen(request, patient_instance)
		if gps_instance == False:
			return render(request, 'patient_create_gps.html', returnVal)

		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_create_gps.html', returnVal)

@login_required(login_url='/login')
def Create_global_psychotrauma_screen(request, patient_instance):
	current_id = request.POST['current_id']
	try:
		new_global_psychotrauma_screen = global_psychotrauma_screen.objects.get(pk=current_id)
	except:
		new_global_psychotrauma_screen = global_psychotrauma_screen()

	new_global_psychotrauma_screen.details = patient_instance
	new_global_psychotrauma_screen.consultation_date = formatDate(request.POST['consultation_date'])
	new_global_psychotrauma_screen.event_description = request.POST['event_description']
	new_global_psychotrauma_screen.event_happened = request.POST['event_happened']

	new_global_psychotrauma_screen.physical_violence = request.POST.get('physical_violence', False)
	new_global_psychotrauma_screen.sexual_violence = request.POST.get('sexual_violence', False)
	new_global_psychotrauma_screen.emotional_abuse = request.POST.get('emotional_abuse', False)
	new_global_psychotrauma_screen.serious_injury = request.POST.get('serious_injury', False)
	new_global_psychotrauma_screen.life_threatening = request.POST.get('life_threatening', False)
	
	new_global_psychotrauma_screen.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False)
	new_global_psychotrauma_screen.cause_harm_to_others = request.POST.get('cause_harm_to_others', False)
	new_global_psychotrauma_screen.covid =  request.POST.get('covid', False)
	new_global_psychotrauma_screen.single_event_occurring = request.POST['single_event_occurring']
	new_global_psychotrauma_screen.range_event_occurring_from = request.POST['range_event_occurring_from']
	new_global_psychotrauma_screen.range_event_occurring_to = request.POST['range_event_occurring_to']
	try:
		new_global_psychotrauma_screen.save()
	except:
		return False

	
	try:
		new_considering_event = considering_event.objects.get(global_psychotrauma_screen=new_global_psychotrauma_screen.pk)
	except:
		new_considering_event = considering_event()
	new_considering_event.global_psychotrauma_screen = new_global_psychotrauma_screen
	new_considering_event.considering_event_1 = request.POST['considering_event_1']
	new_considering_event.considering_event_2 = request.POST['considering_event_2']
	new_considering_event.considering_event_3 = request.POST['considering_event_3']
	new_considering_event.considering_event_4 = request.POST['considering_event_4']
	new_considering_event.considering_event_5 = request.POST['considering_event_5']
	new_considering_event.considering_event_6 = request.POST['considering_event_6']
	new_considering_event.considering_event_7 = request.POST['considering_event_7']
	new_considering_event.considering_event_8 = request.POST['considering_event_8']
	new_considering_event.considering_event_9 = request.POST['considering_event_9']
	new_considering_event.considering_event_10 = request.POST['considering_event_10']
	new_considering_event.considering_event_11 = request.POST['considering_event_11']
	new_considering_event.considering_event_12 = request.POST['considering_event_12']
	new_considering_event.considering_event_13 = request.POST['considering_event_13']
	new_considering_event.considering_event_14 = request.POST['considering_event_14']
	new_considering_event.considering_event_15 = request.POST['considering_event_15']
	new_considering_event.considering_event_16 = request.POST['considering_event_16']
	new_considering_event.considering_event_17 = request.POST['considering_event_17']
	new_considering_event.considering_event_18 = request.POST['considering_event_18']
	new_considering_event.considering_event_19 = request.POST['considering_event_19']
	new_considering_event.considering_event_20 = request.POST['considering_event_20']
	new_considering_event.considering_event_21 = request.POST['considering_event_21']
	new_considering_event.considering_event_22 = request.POST['considering_event_22']
	new_considering_event.considering_event_23 = request.POST['considering_event_23']
	try:
		new_considering_event.save()
	except:
		new_global_psychotrauma_screen.delete()
		return False

@login_required(login_url="/login")
def PatientAutoSaveGPS(request):
	returnVal = {}
	returnVal['status_code'] = 0
	patient_id = request.POST['patient_id']
	current_id = request.POST['current_id']
	print(current_id)
	if current_id != "0":
		try:
			gps_details = global_psychotrauma_screen.objects.get(pk=current_id)
		except:
			returnVal['error_msg'] = "id does not exists"
			return JsonResponse(returnVal, safe=False)
		
		gps_details.consultation_date = formatDate(request.POST['consultation_date'])
		gps_details.event_description = request.POST['event_description']
		gps_details.event_happened = request.POST['event_happened']

		gps_details.physical_violence = request.POST.get('physical_violence', False)
		gps_details.sexual_violence = request.POST.get('sexual_violence', False)
		gps_details.emotional_abuse = request.POST.get('emotional_abuse', False)
		gps_details.serious_injury = request.POST.get('serious_injury', False)
		gps_details.life_threatening = request.POST.get('life_threatening', False)
		
		gps_details.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False)
		gps_details.cause_harm_to_others = request.POST.get('cause_harm_to_others', False)
		gps_details.covid =  request.POST.get('covid', False)
		gps_details.single_event_occurring = request.POST['single_event_occurring']
		gps_details.range_event_occurring_from = request.POST['range_event_occurring_from']
		gps_details.range_event_occurring_to = request.POST['range_event_occurring_to']
		try:
			gps_details.save()
		except:
			returnVal['error_msg'] = "Error on saving gps"
			return JsonResponse(returnVal, safe=False)

		considering_event_details = considering_event.objects.get(global_psychotrauma_screen=gps_details.pk)
		considering_event_details.considering_event_1 = request.POST.get('considering_event_1', False)
		considering_event_details.considering_event_2 = request.POST.get('considering_event_2', False)
		considering_event_details.considering_event_3 = request.POST.get('considering_event_3', False)
		considering_event_details.considering_event_4 = request.POST.get('considering_event_4', False)
		considering_event_details.considering_event_5 = request.POST.get('considering_event_5', False)
		considering_event_details.considering_event_6 = request.POST.get('considering_event_6', False)
		considering_event_details.considering_event_7 = request.POST.get('considering_event_7', False)
		considering_event_details.considering_event_8 = request.POST.get('considering_event_8', False)
		considering_event_details.considering_event_9 = request.POST.get('considering_event_9', False)
		considering_event_details.considering_event_10 = request.POST.get('considering_event_10', False)
		considering_event_details.considering_event_11 = request.POST.get('considering_event_11', False)
		considering_event_details.considering_event_12 = request.POST.get('considering_event_12', False)
		considering_event_details.considering_event_13 = request.POST.get('considering_event_13', False)
		considering_event_details.considering_event_14 = request.POST.get('considering_event_14', False)
		considering_event_details.considering_event_15 = request.POST.get('considering_event_15', False)
		considering_event_details.considering_event_16 = request.POST.get('considering_event_16', False)
		considering_event_details.considering_event_17 = request.POST.get('considering_event_17', False)
		considering_event_details.considering_event_18 = request.POST.get('considering_event_18', False)
		considering_event_details.considering_event_19 = request.POST.get('considering_event_19', False)
		considering_event_details.considering_event_20 = request.POST.get('considering_event_20', False)
		considering_event_details.considering_event_21 = request.POST.get('considering_event_21', False)
		considering_event_details.considering_event_22 = request.POST.get('considering_event_22', False)
		considering_event_details.considering_event_23 = request.POST.get('considering_event_23', False)
		try:
			considering_event_details.save()
		except:
			new_global_psychotrauma_screen.delete()
			returnVal['error_msg'] = "Error on saving gps screen"
			return JsonResponse(returnVal, safe=False)

		returnVal['current_id'] = current_id
		return JsonResponse(returnVal, safe=False)

	else:
		try:
			patient_instance = details.objects.get(pk=patient_id)
		except:
			returnVal['error_msg'] = "patient_id does not exists"
			return JsonResponse(returnVal, safe=False)

		new_global_psychotrauma_screen = global_psychotrauma_screen()
		new_global_psychotrauma_screen.details = patient_instance
		new_global_psychotrauma_screen.consultation_date = formatDate(request.POST['consultation_date'])
		new_global_psychotrauma_screen.event_description = request.POST['event_description']
		new_global_psychotrauma_screen.event_happened = request.POST['event_happened']

		new_global_psychotrauma_screen.physical_violence = request.POST.get('physical_violence', False)
		new_global_psychotrauma_screen.sexual_violence = request.POST.get('sexual_violence', False)
		new_global_psychotrauma_screen.emotional_abuse = request.POST.get('emotional_abuse', False)
		new_global_psychotrauma_screen.serious_injury = request.POST.get('serious_injury', False)
		new_global_psychotrauma_screen.life_threatening = request.POST.get('life_threatening', False)
		
		new_global_psychotrauma_screen.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False)
		new_global_psychotrauma_screen.cause_harm_to_others = request.POST.get('cause_harm_to_others', False)
		new_global_psychotrauma_screen.covid =  request.POST.get('covid', False)
		new_global_psychotrauma_screen.single_event_occurring = request.POST['single_event_occurring']
		new_global_psychotrauma_screen.range_event_occurring_from = request.POST['range_event_occurring_from']
		new_global_psychotrauma_screen.range_event_occurring_to = request.POST['range_event_occurring_to']
		try:
			new_global_psychotrauma_screen.save()
			returnVal['current_id'] = new_global_psychotrauma_screen.pk
		except:
			returnVal['error_msg'] = "Error on saving gps"
			return JsonResponse(returnVal, safe=False)

		new_considering_event = considering_event()
		new_considering_event.global_psychotrauma_screen = new_global_psychotrauma_screen
		new_considering_event.considering_event_1 = request.POST.get('considering_event_1', False)
		new_considering_event.considering_event_2 = request.POST.get('considering_event_2', False)
		new_considering_event.considering_event_3 = request.POST.get('considering_event_3', False)
		new_considering_event.considering_event_4 = request.POST.get('considering_event_4', False)
		new_considering_event.considering_event_5 = request.POST.get('considering_event_5', False)
		new_considering_event.considering_event_6 = request.POST.get('considering_event_6', False)
		new_considering_event.considering_event_7 = request.POST.get('considering_event_7', False)
		new_considering_event.considering_event_8 = request.POST.get('considering_event_8', False)
		new_considering_event.considering_event_9 = request.POST.get('considering_event_9', False)
		new_considering_event.considering_event_10 = request.POST.get('considering_event_10', False)
		new_considering_event.considering_event_11 = request.POST.get('considering_event_11', False)
		new_considering_event.considering_event_12 = request.POST.get('considering_event_12', False)
		new_considering_event.considering_event_13 = request.POST.get('considering_event_13', False)
		new_considering_event.considering_event_14 = request.POST.get('considering_event_14', False)
		new_considering_event.considering_event_15 = request.POST.get('considering_event_15', False)
		new_considering_event.considering_event_16 = request.POST.get('considering_event_16', False)
		new_considering_event.considering_event_17 = request.POST.get('considering_event_17', False)
		new_considering_event.considering_event_18 = request.POST.get('considering_event_18', False)
		new_considering_event.considering_event_19 = request.POST.get('considering_event_19', False)
		new_considering_event.considering_event_20 = request.POST.get('considering_event_20', False)
		new_considering_event.considering_event_21 = request.POST.get('considering_event_21', False)
		new_considering_event.considering_event_22 = request.POST.get('considering_event_22', False)
		new_considering_event.considering_event_23 = request.POST.get('considering_event_23', False)
		try:
			new_considering_event.save()
		except:
			new_global_psychotrauma_screen.delete()
			returnVal['error_msg'] = "Error on saving gps screen"
			return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)


@login_required(login_url="/login")
def PatientAutoSaveHamd(request):
	returnVal = {}
	returnVal['status_code'] = 0
	patient_id = request.POST['patient_id']
	current_id = request.POST['current_id']

	if current_id != "0":
		score = 0
		total_score = 0
		new_hamd = hamd.objects.get(pk=current_id)
		new_hamd.depressed_mood = request.POST.get('depressed_mood', False)
		if new_hamd.depressed_mood != False:
			score = score + int(new_hamd.depressed_mood)

		new_hamd.feeling_of_guilt = request.POST.get('feeling_of_guilt', False)
		if new_hamd.feeling_of_guilt != False: 
			score = score + int(new_hamd.feeling_of_guilt)

		new_hamd.suicide = request.POST.get('suicide', False)
		if new_hamd.suicide != False: 
			score = score + int(new_hamd.suicide)

		new_hamd.insomnia_initial = request.POST.get('insomnia_initial', False)
		if new_hamd.insomnia_initial != False: 
			score = score + int(new_hamd.insomnia_initial)


		new_hamd.insomnia_middle = request.POST.get('insomnia_middle', False)
		if new_hamd.insomnia_middle != False: 
			score = score + int(new_hamd.insomnia_middle)

		new_hamd.insomnia_delayed = request.POST.get('insomnia_delayed', False)
		if new_hamd.insomnia_delayed != False: 
			score = score + int(new_hamd.insomnia_delayed)

		new_hamd.work_and_interests = request.POST.get('work_and_interests', False)
		if new_hamd.work_and_interests != False: 
			score = score + int(new_hamd.work_and_interests)

		new_hamd.retardation_delayed = request.POST.get('retardation_delayed', False)
		if new_hamd.retardation_delayed != False: 
			score = score + int(new_hamd.retardation_delayed)

		new_hamd.agitation_delayed = request.POST.get('agitation_delayed', False)
		if new_hamd.agitation_delayed != False: 
			score = score + int(new_hamd.agitation_delayed)

		new_hamd.anxiety_psychic = request.POST.get('anxiety_psychic', False)
		if new_hamd.anxiety_psychic != False: 
			score = score + int(new_hamd.anxiety_psychic)

		new_hamd.anxiety_somatic = request.POST.get('anxiety_somatic', False)
		if new_hamd.anxiety_somatic != False: 
			score = score + int(new_hamd.anxiety_somatic)

		new_hamd.somatic_symptoms_gastrointestinal = request.POST.get('somatic_symptoms_gastrointestinal', False)
		if new_hamd.somatic_symptoms_gastrointestinal != False: 
			score = score + int(new_hamd.somatic_symptoms_gastrointestinal)

		new_hamd.somatic_symptoms_general = request.POST.get('somatic_symptoms_general', False)
		if new_hamd.somatic_symptoms_general != False: 
			score = score + int(new_hamd.somatic_symptoms_general)

		new_hamd.genital_symptoms = request.POST.get('genital_symptoms', False)
		if new_hamd.genital_symptoms != False: 
			score = score + int(new_hamd.genital_symptoms)

		new_hamd.hypochondriasis = request.POST.get('hypochondriasis', False)
		if new_hamd.hypochondriasis != False: 
			score = score + int(new_hamd.hypochondriasis)

		new_hamd.weight_loss = request.POST.get('weight_loss', False)
		if new_hamd.weight_loss != False: 
			score = score + int(new_hamd.weight_loss)

		new_hamd.insight = request.POST.get('insight', False)
		if new_hamd.insight != False: 
			score = score + int(new_hamd.insight)

		new_hamd.diurnal_variation = request.POST.get('diurnal_variation', False)
		if new_hamd.diurnal_variation != False: 
			score = score + int(new_hamd.diurnal_variation)

		new_hamd.score = score
		total_score = score

		new_hamd.diurnal_variation_mild_am = request.POST.get('diurnal_variation_mild_am', False)
		new_hamd.diurnal_variation_mild_pm = request.POST.get('diurnal_variation_mild_pm', False)
		new_hamd.diurnal_variation_severe_am = request.POST.get('diurnal_variation_severe_am', False)
		new_hamd.diurnal_variation_severe_pm = request.POST.get('diurnal_variation_severe_pm', False)

		new_hamd.depersonalization_and_derelization = request.POST.get('depersonalization_and_derelization', False)
		if new_hamd.depersonalization_and_derelization != False: 
			total_score = total_score + int(new_hamd.depersonalization_and_derelization)

		new_hamd.paranoid_symptoms = request.POST.get('paranoid_symptoms', False)
		if new_hamd.paranoid_symptoms != False: 
			total_score = total_score + int(new_hamd.paranoid_symptoms)

		new_hamd.obsessional_symptoms = request.POST.get('obsessional_symptoms', False)
		if new_hamd.obsessional_symptoms != False: 
			total_score = total_score + int(new_hamd.obsessional_symptoms)
		new_hamd.total_score = total_score
		try:
			new_hamd.save()
			returnVal['current_id'] = current_id
		except:
			returnVal['error_msg'] = "Error on saving hamd Data"
			return JsonResponse(returnVal, safe=False)
	else:
		score = 0
		total_score = 0
		new_hamd = hamd()
		new_hamd.consultation_date = formatDate(request.POST['consultation_date'])
		try:
			patient_instance = details.objects.get(pk=patient_id)
		except:
			returnVal['error_msg'] = "patient_id does not exists"
			return JsonResponse(returnVal, safe=False)
		new_hamd.details = patient_instance

		new_hamd.depressed_mood = request.POST.get('depressed_mood', False)
		if new_hamd.depressed_mood != False:
			score = score + int(new_hamd.depressed_mood)

		new_hamd.feeling_of_guilt = request.POST.get('feeling_of_guilt', False)
		if new_hamd.feeling_of_guilt != False: 
			score = score + int(new_hamd.feeling_of_guilt)

		new_hamd.suicide = request.POST.get('suicide', False)
		if new_hamd.suicide != False: 
			score = score + int(new_hamd.suicide)

		new_hamd.insomnia_initial = request.POST.get('insomnia_initial', False)
		if new_hamd.insomnia_initial != False: 
			score = score + int(new_hamd.insomnia_initial)


		new_hamd.insomnia_middle = request.POST.get('insomnia_middle', False)
		if new_hamd.insomnia_middle != False: 
			score = score + int(new_hamd.insomnia_middle)

		new_hamd.insomnia_delayed = request.POST.get('insomnia_delayed', False)
		if new_hamd.insomnia_delayed != False: 
			score = score + int(new_hamd.insomnia_delayed)

		new_hamd.work_and_interests = request.POST.get('work_and_interests', False)
		if new_hamd.work_and_interests != False: 
			score = score + int(new_hamd.work_and_interests)

		new_hamd.retardation_delayed = request.POST.get('retardation_delayed', False)
		if new_hamd.retardation_delayed != False: 
			score = score + int(new_hamd.retardation_delayed)

		new_hamd.agitation_delayed = request.POST.get('agitation_delayed', False)
		if new_hamd.agitation_delayed != False: 
			score = score + int(new_hamd.agitation_delayed)

		new_hamd.anxiety_psychic = request.POST.get('anxiety_psychic', False)
		if new_hamd.anxiety_psychic != False: 
			score = score + int(new_hamd.anxiety_psychic)

		new_hamd.anxiety_somatic = request.POST.get('anxiety_somatic', False)
		if new_hamd.anxiety_somatic != False: 
			score = score + int(new_hamd.anxiety_somatic)

		new_hamd.somatic_symptoms_gastrointestinal = request.POST.get('somatic_symptoms_gastrointestinal', False)
		if new_hamd.somatic_symptoms_gastrointestinal != False: 
			score = score + int(new_hamd.somatic_symptoms_gastrointestinal)

		new_hamd.somatic_symptoms_general = request.POST.get('somatic_symptoms_general', False)
		if new_hamd.somatic_symptoms_general != False: 
			score = score + int(new_hamd.somatic_symptoms_general)

		new_hamd.genital_symptoms = request.POST.get('genital_symptoms', False)
		if new_hamd.genital_symptoms != False: 
			score = score + int(new_hamd.genital_symptoms)

		new_hamd.hypochondriasis = request.POST.get('hypochondriasis', False)
		if new_hamd.hypochondriasis != False: 
			score = score + int(new_hamd.hypochondriasis)

		new_hamd.weight_loss = request.POST.get('weight_loss', False)
		if new_hamd.weight_loss != False: 
			score = score + int(new_hamd.weight_loss)

		new_hamd.insight = request.POST.get('insight', False)
		if new_hamd.insight != False: 
			score = score + int(new_hamd.insight)

		new_hamd.diurnal_variation = request.POST.get('diurnal_variation', False)
		if new_hamd.diurnal_variation != False: 
			score = score + int(new_hamd.diurnal_variation)

		new_hamd.score = score
		total_score = score

		new_hamd.diurnal_variation_mild_am = request.POST.get('diurnal_variation_mild_am', False)
		new_hamd.diurnal_variation_mild_pm = request.POST.get('diurnal_variation_mild_pm', False)
		new_hamd.diurnal_variation_severe_am = request.POST.get('diurnal_variation_severe_am', False)
		new_hamd.diurnal_variation_severe_pm = request.POST.get('diurnal_variation_severe_pm', False)

		new_hamd.depersonalization_and_derelization = request.POST.get('depersonalization_and_derelization', False)
		if new_hamd.depersonalization_and_derelization != False: 
			total_score = total_score + int(new_hamd.depersonalization_and_derelization)

		new_hamd.paranoid_symptoms = request.POST.get('paranoid_symptoms', False)
		if new_hamd.paranoid_symptoms != False: 
			total_score = total_score + int(new_hamd.paranoid_symptoms)

		new_hamd.obsessional_symptoms = request.POST.get('obsessional_symptoms', False)
		if new_hamd.obsessional_symptoms != False: 
			total_score = total_score + int(new_hamd.obsessional_symptoms)
		new_hamd.total_score = total_score
		try:
			new_hamd.save()
			returnVal['current_id'] = new_hamd.pk
		except:
			returnVal['error_msg'] = "Error on saving hamd Data"
			return JsonResponse(returnVal, safe=False)

	return JsonResponse(returnVal, safe=False)


@login_required(login_url='/login')
def PatientUpdateGPS(request, gps_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['current_id'] = gps_id
	global_psychotrauma_screen_instance = global_psychotrauma_screen.objects.get(pk=gps_id)
	
	try:
		global_psychotrauma_screen_instance = global_psychotrauma_screen.objects.get(pk=gps_id)
		returnVal['global_psychotrauma_screen_instance'] = global_psychotrauma_screen_instance
	except:
		returnVal['error_msg'] = "Global Psychotrauma Screen Data does not exists"
		return render(request, 'patient_edit_gps.html', returnVal)

	try:
		patient_instance = details.objects.get(pk=global_psychotrauma_screen_instance.details.pk)
		returnVal['patientDetail'] = patient_instance
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_edit_gps.html', returnVal)
		
	try:
		considering_event_instance = considering_event.objects.get(global_psychotrauma_screen=gps_id)
		returnVal['considering_event_instance'] = considering_event_instance
	except:
		returnVal['error_msg'] = "Considering Event Data does not exists"
		return render(request, 'patient_edit_gps.html', returnVal)

	if request.method == "POST":
		global_psychotrauma_screen_instance.event_description = request.POST['event_description']
		global_psychotrauma_screen_instance.event_happened = request.POST['event_happened']

		global_psychotrauma_screen_instance.physical_violence = request.POST.get('physical_violence', False)
		global_psychotrauma_screen_instance.sexual_violence = request.POST.get('sexual_violence', False)
		global_psychotrauma_screen_instance.emotional_abuse = request.POST.get('emotional_abuse', False)
		global_psychotrauma_screen_instance.serious_injury = request.POST.get('serious_injury', False)
		global_psychotrauma_screen_instance.life_threatening = request.POST.get('life_threatening', False)


		global_psychotrauma_screen_instance.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False)
		global_psychotrauma_screen_instance.cause_harm_to_others = request.POST.get('cause_harm_to_others', False)
		global_psychotrauma_screen_instance.covid =  request.POST.get('covid', False)
		global_psychotrauma_screen_instance.single_event_occurring = request.POST['single_event_occurring']
		global_psychotrauma_screen_instance.range_event_occurring_from = request.POST['range_event_occurring_from']
		global_psychotrauma_screen_instance.range_event_occurring_to = request.POST['range_event_occurring_to']
		try:
			global_psychotrauma_screen_instance.save()
		except:
			returnVal['error_msg'] = "error on Saving the GPS Data!"
			return render(request, 'patient_edit_gps.html', returnVal)

		considering_event_instance.considering_event_1 = request.POST['considering_event_1']
		considering_event_instance.considering_event_2 = request.POST['considering_event_2']
		considering_event_instance.considering_event_3 = request.POST['considering_event_3']
		considering_event_instance.considering_event_4 = request.POST['considering_event_4']
		considering_event_instance.considering_event_5 = request.POST['considering_event_5']
		considering_event_instance.considering_event_6 = request.POST['considering_event_6']
		considering_event_instance.considering_event_7 = request.POST['considering_event_7']
		considering_event_instance.considering_event_8 = request.POST['considering_event_8']
		considering_event_instance.considering_event_9 = request.POST['considering_event_9']
		considering_event_instance.considering_event_10 = request.POST['considering_event_10']
		considering_event_instance.considering_event_11 = request.POST['considering_event_11']
		considering_event_instance.considering_event_12 = request.POST['considering_event_12']
		considering_event_instance.considering_event_13 = request.POST['considering_event_13']
		considering_event_instance.considering_event_14 = request.POST['considering_event_14']
		considering_event_instance.considering_event_15 = request.POST['considering_event_15']
		considering_event_instance.considering_event_16 = request.POST['considering_event_16']
		considering_event_instance.considering_event_17 = request.POST['considering_event_17']
		considering_event_instance.considering_event_18 = request.POST['considering_event_18']
		considering_event_instance.considering_event_19 = request.POST['considering_event_19']
		considering_event_instance.considering_event_20 = request.POST['considering_event_20']
		considering_event_instance.considering_event_21 = request.POST['considering_event_21']
		considering_event_instance.considering_event_22 = request.POST['considering_event_22']
		considering_event_instance.considering_event_23 = request.POST['considering_event_23']
		try:
			considering_event_instance.save()
		except:
			returnVal['error_msg'] = "error on Saving the GPS Data!"
			return render(request, 'patient_edit_gps.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_edit_gps.html', returnVal)

@login_required(login_url='/login')
def PatientCreateHamD(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['patientId'] = patient_id
	
	try:
		patient_instance = details.objects.get(pk=patient_id)
		returnVal['patientDetail'] = patient_instance
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_create_hamd.html', returnVal)

	if request.method == "POST":
		current_id = request.POST['current_id']
		score = 0
		total_score = 0
		try:
			new_hamd = hamd.objects.get(pk=current_id)
		except:
			new_hamd = hamd()
			
		new_hamd.consultation_date = formatDate(request.POST['consultation_date'])
		new_hamd.details = patient_instance
		new_hamd.depressed_mood = request.POST['depressed_mood']
		score = score + int(new_hamd.depressed_mood)
		new_hamd.feeling_of_guilt = request.POST['feeling_of_guilt']
		score = score + int(new_hamd.feeling_of_guilt)
		new_hamd.suicide = request.POST['suicide']
		score = score + int(new_hamd.suicide)
		new_hamd.insomnia_initial = request.POST['insomnia_initial']
		score = score + int(new_hamd.insomnia_initial)
		new_hamd.insomnia_middle = request.POST['insomnia_middle']
		score = score + int(new_hamd.insomnia_middle)
		new_hamd.insomnia_delayed = request.POST['insomnia_delayed']
		score = score + int(new_hamd.insomnia_delayed)
		new_hamd.work_and_interests = request.POST['work_and_interests']
		score = score + int(new_hamd.work_and_interests)
		new_hamd.retardation_delayed = request.POST['retardation_delayed']
		score = score + int(new_hamd.retardation_delayed)
		new_hamd.agitation_delayed = request.POST['agitation_delayed']
		score = score + int(new_hamd.agitation_delayed)
		new_hamd.anxiety_psychic = request.POST['anxiety_psychic']
		score = score + int(new_hamd.anxiety_psychic)
		new_hamd.anxiety_somatic = request.POST['anxiety_somatic']
		score = score + int(new_hamd.anxiety_somatic)
		new_hamd.somatic_symptoms_gastrointestinal = request.POST['somatic_symptoms_gastrointestinal']
		score = score + int(new_hamd.somatic_symptoms_gastrointestinal)
		new_hamd.somatic_symptoms_general = request.POST['somatic_symptoms_general']
		score = score + int(new_hamd.somatic_symptoms_general)
		new_hamd.genital_symptoms = request.POST['genital_symptoms']
		score = score + int(new_hamd.genital_symptoms)
		new_hamd.hypochondriasis = request.POST['hypochondriasis']
		score = score + int(new_hamd.hypochondriasis)
		new_hamd.weight_loss = request.POST['weight_loss']
		score = score + int(new_hamd.weight_loss)
		new_hamd.insight = request.POST['insight']
		score = score + int(new_hamd.insight)
		new_hamd.score = score
		total_score = score
		new_hamd.diurnal_variation = request.POST['diurnal_variation']
		total_score = total_score + int(new_hamd.diurnal_variation)

		new_hamd.diurnal_variation_mild_am = request.POST.get('diurnal_variation_mild_am', False)
		new_hamd.diurnal_variation_mild_pm = request.POST.get('diurnal_variation_mild_pm', False)
		new_hamd.diurnal_variation_severe_am = request.POST.get('diurnal_variation_severe_am', False)
		new_hamd.diurnal_variation_severe_pm = request.POST.get('diurnal_variation_severe_pm', False)

		new_hamd.depersonalization_and_derelization = request.POST['depersonalization_and_derelization']
		total_score = total_score + int(new_hamd.depersonalization_and_derelization)
		new_hamd.paranoid_symptoms = request.POST['paranoid_symptoms']
		total_score = total_score + int(new_hamd.paranoid_symptoms)
		new_hamd.obsessional_symptoms = request.POST['obsessional_symptoms']
		total_score = total_score + int(new_hamd.obsessional_symptoms)
		new_hamd.total_score = total_score
		try:
			new_hamd.save()
		except:
			returnVal['error_msg'] = "Error on saving hamd Data"
			return render(request, 'patient_create_hamd.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_create_hamd.html', returnVal)


@login_required(login_url='/login')
def PatientUpdateHamD(request, hamd_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['current_id'] = hamd_id
	try:
		hamd_details = hamd.objects.get(pk=hamd_id)
	except:
		returnVal['error_msg'] = "Error HAMD data does not exists!"
		return render(request, 'patient_edit_hamd.html', returnVal)
	returnVal['hamd_details'] = hamd_details
	try:
		patient_instance = details.objects.get(pk=hamd_details.details.pk)
		returnVal['patientDetail'] = patient_instance
	except:
		returnVal['error_msg'] = "Patient does not exists"
		return render(request, 'patient_edit_hamd.html', returnVal)

	if request.method == "POST":
		score = 0
		total_score = 0
		hamd_details.consultation_date = formatDate(request.POST['consultation_date'])
		hamd_details.depressed_mood = request.POST['depressed_mood']
		score = score + int(hamd_details.depressed_mood)
		hamd_details.feeling_of_guilt = request.POST['feeling_of_guilt']
		score = score + int(hamd_details.feeling_of_guilt)
		hamd_details.suicide = request.POST['suicide']
		score = score + int(hamd_details.suicide)
		hamd_details.insomnia_initial = request.POST['insomnia_initial']
		score = score + int(hamd_details.insomnia_initial)
		hamd_details.insomnia_middle = request.POST['insomnia_middle']
		score = score + int(hamd_details.insomnia_middle)
		hamd_details.insomnia_delayed = request.POST['insomnia_delayed']
		score = score + int(hamd_details.insomnia_delayed)
		hamd_details.work_and_interests = request.POST['work_and_interests']
		score = score + int(hamd_details.work_and_interests)
		hamd_details.retardation_delayed = request.POST['retardation_delayed']
		score = score + int(hamd_details.retardation_delayed)
		hamd_details.agitation_delayed = request.POST['agitation_delayed']
		score = score + int(hamd_details.agitation_delayed)
		hamd_details.anxiety_psychic = request.POST['anxiety_psychic']
		score = score + int(hamd_details.anxiety_psychic)
		hamd_details.anxiety_somatic = request.POST['anxiety_somatic']
		score = score + int(hamd_details.anxiety_somatic)
		hamd_details.somatic_symptoms_gastrointestinal = request.POST['somatic_symptoms_gastrointestinal']
		score = score + int(hamd_details.somatic_symptoms_gastrointestinal)
		hamd_details.somatic_symptoms_general = request.POST['somatic_symptoms_general']
		score = score + int(hamd_details.somatic_symptoms_general)
		hamd_details.genital_symptoms = request.POST['genital_symptoms']
		score = score + int(hamd_details.genital_symptoms)
		hamd_details.hypochondriasis = request.POST['hypochondriasis']
		score = score + int(hamd_details.hypochondriasis)
		hamd_details.weight_loss = request.POST['weight_loss']
		score = score + int(hamd_details.weight_loss)
		hamd_details.insight = request.POST['insight']
		score = score + int(hamd_details.insight)
		hamd_details.score = score
		total_score = score
		hamd_details.diurnal_variation = request.POST['diurnal_variation']
		total_score = total_score + int(hamd_details.diurnal_variation)

		hamd_details.diurnal_variation_mild_am = request.POST.get('diurnal_variation_mild_am', False)
		hamd_details.diurnal_variation_mild_pm = request.POST.get('diurnal_variation_mild_pm', False)
		hamd_details.diurnal_variation_severe_am = request.POST.get('diurnal_variation_severe_am', False)
		hamd_details.diurnal_variation_severe_pm = request.POST.get('diurnal_variation_severe_pm', False)

		hamd_details.depersonalization_and_derelization = request.POST['depersonalization_and_derelization']
		total_score = total_score + int(hamd_details.depersonalization_and_derelization)
		hamd_details.paranoid_symptoms = request.POST['paranoid_symptoms']
		total_score = total_score + int(hamd_details.paranoid_symptoms)
		hamd_details.obsessional_symptoms = request.POST['obsessional_symptoms']
		total_score = total_score + int(hamd_details.obsessional_symptoms)
		hamd_details.total_score = total_score
		try:
			hamd_details.save()
		except:
			returnVal['error_msg'] = "Error on saving hamd Data"
			return render(request, 'patient_create_hamd.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)

	return render(request, 'patient_edit_hamd.html', returnVal)

@login_required(login_url='/login')
def PatientGetGPS(request):
	returnVal = {}
	gps_id = request.GET['gps_id']
	try:
		returnVal['gps_details'] = global_psychotrauma_screen.objects.get(pk=gps_id)
		returnVal['considering_event_details'] = considering_event.objects.get(global_psychotrauma_screen=gps_id)
	except:
		return False

	html = render_to_string('patient_gps_details.html', returnVal)
	return HttpResponse(html)

@login_required(login_url='/login')
def PatientGetHamd(request):
	returnVal = {}
	hamd_id = request.GET['hamd_id']
	try:
		returnVal['hamd_details'] = hamd.objects.get(pk=hamd_id)
	except:
		return False

	html = render_to_string('patient_hamd_details.html', returnVal)
	return HttpResponse(html)

@login_required(login_url='/login')
def PatientRemoveRelative(request):
	returnVal = {}
	returnVal['status_code'] = 0
	try:
		relative_details = relatives.objects.get(pk=request.GET['relative_id'])
	except:
		returnVal['error_msg'] = "Relative Does not exists!"
		return JsonResponse(returnVal, safe=False)
	relative_details.status = 0
	relative_details.is_delete = 1
	try:
		relative_details.save()
		returnVal['status_code'] = 0
		return JsonResponse(returnVal, safe=False)
	except:
		returnVal['error_msg'] = "Error on saving!"
		return JsonResponse(returnVal, safe=False)

@login_required(login_url='/login')
def PatientDeleteAllergy(request):
	returnVal = {}
	returnVal['status_code'] = 0
	try:
		allergies_details = relatives.objects.get(pk=request.GET['allergy_id'])
	except:
		returnVal['error_msg'] = "Allergy Does not exists!"
		return JsonResponse(returnVal, safe=False)
	allergies_details.status = 0
	allergies_details.is_delete = 1
	try:
		allergies_details.save()
		returnVal['status_code'] = 0
		return JsonResponse(returnVal, safe=False)
	except:
		returnVal['error_msg'] = "Error on saving!"
		return JsonResponse(returnVal, safe=False)


@login_required(login_url='/login')
def PatientFileUpload(request):
	returnVal = {}
	if request.method == "POST":
		form = patientFilesForm(request.POST, request.FILES)
		if form.is_valid():
			print("here")
			try:
				patient_instance = details.objects.get(pk=request.POST['patient_id'])
			except:
				returnVal['error_msg'] = "Encounter Does not exists"
				return render(request, 'error_page.html', returnVal)

			formPost = form.save(commit=False)
			formPost.details = patient_instance
			formPost.save()

			return redirect("PatientDetailed", patient_id=request.POST['patient_id'])
		else:
			return redirect("PatientDetailed", patient_id=request.POST['patient_id'])
	else:
		returnVal['error_msg'] = "Encounter Does not exists"
		return render(request, 'error_page.html', returnVal)

@login_required(login_url='/login')
def referralFormPdf(request, referral_id):
	# # Define the data to be passed to the template
	# context = {
	# 	'title': 'Sample PDF Document',
	# 	'content': 'This is a sample content in the PDF document.'
	# }
	# # Render the HTML template with context data
	# html = render_to_string('referral_form.html', context)
	# # Create a response object for the PDF
	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'inline; filename="output.pdf"'
	# # Generate the PD
	# pisa_status = pisa.CreatePDF(html, dest=response)
	# # If an error occurs, show it
	# if pisa_status.err:
	# 	return HttpResponse('We had some errors <pre>' + html + '</pre>')

	return false

@login_required(login_url='/login')
def PatientViewSurvey(request, patient_id):
	returnVal = {}
	try:
		returnVal['survey_details'] = patient_survey.objects.get(details=patient_id);
	except:
		returnVal['error_msg'] = "Error on saving hamd Data"
	return render(request, 'patient_survey_view.html', returnVal)

def PatientSurveyCompleted(request):
	return render(request, 'patient_survey_complete.html')

def PatientSurvey(request, patient_id):
	returnVal = {}
	returnVal['form'] = patientSurveyForm()

	try:
		patient_instance = details.objects.get(pk=patient_id)
	except:
		return redirect("dashboard")

	if request.method == "POST":
		form = patientSurveyForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.details = patient_instance
			post.save()
			return render(request, 'patient_survey_complete.html')
	try: 
		taken_survey = patient_survey.objects.get(details=patient_instance.pk)
		return render(request, 'patient_survey_complete.html')
	except:
		return render(request, 'patient_survey.html', returnVal)



def formatDate(dateValue):
	current_date_split = dateValue.split("/")
	if len(current_date_split) == 3:
		return current_date_split[2]+"-"+current_date_split[0]+"-"+current_date_split[1]
	else:
		return False





	