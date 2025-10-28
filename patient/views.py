from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import date, datetime
from django.utils.timezone import now 
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey, details_audit, details_files
from patient.patient_forms import AddRelativesForm, EditRelativesForm, AddPatientForm, AddPatientAddressForm, EditPatientForm, EditPatientAddressForm, patientSurveyForm, patientFilesForm
from consultation.models import encounter, Referral, diagnosis, treatment, history_present_illness
import random, os, json, ast


from datetime import date, datetime


@login_required(login_url='/login')
def PatientLists(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
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

	if workplace_choice:  # Filter by workplace if it's not None
		list_of_patients = details.objects.filter(
			is_delete=0,
			workplace=workplace_choice  # Filter by the workplace field in related 'details'
		)
	else:
		# If no specific workplace is set (e.g., for "Doctor", "Triage", or "Admin"), skip the workplace filter
		list_of_patients = details.objects.filter(
			is_delete=0
		)
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
		PatientAuditTrail(request ,patient_instance, request.POST)
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
			return render(request, 'patient_edit.html', returnVal)
	return render(request, 'patient_edit.html', returnVal)

def PatientAuditTrail(request, patient_old_details, formDetails):
	# Create an empty dictionary to store the audit trail
	profile_details = User.objects.get(pk=request.user.id)
	updated_fields = {}
	# Iterate over the fields in formDetails
	for field, new_value in formDetails.items():
		if hasattr(patient_old_details, field):
			old_value = getattr(patient_old_details, field)
			if isinstance(old_value, date):
				try:
					new_date_value = datetime.strptime(new_value, '%m/%d/%Y').date()
					if old_value != new_date_value:
						updated_fields[field] = {
							'old_value': serialize_value(old_value),
							'new_value': serialize_value(new_date_value)
						}
				except ValueError:
					continue

			else:
				if str(old_value) != str(new_value):  # formDetails values are lists
					updated_fields[field] = {
						'old_value': serialize_value(old_value),
						'new_value': serialize_value(new_value)
					}
	if updated_fields:
		new_audit_entry = details_audit()
		new_audit_entry.user = request.user
		new_audit_entry.url = "patient_edit"
		new_audit_entry.details = patient_old_details
		new_audit_entry.updated_fields= json.dumps(updated_fields)
		new_audit_entry.create_date=now()
		new_audit_entry.status=True
		new_audit_entry.is_delete=False
		new_audit_entry.save()
	return False


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
	try:
		GPS = global_psychotrauma_screen.objects.get(details=patient_id, is_delete=0)
		GPS_CE = considering_event.objects.get(global_psychotrauma_screen=GPS.pk)
		returnVal['GPS_CE_score'] = GPS_CE.score_1_16

	except:
		returnVal['GPS_CE_score'] = 0

	returnVal['list_of_GPS'] = global_psychotrauma_screen.objects.filter(details=patient_id, is_delete=0)
	patientHistory = details_audit.objects.filter(details=patient_id, is_delete=0)

	for history in patientHistory:
		if isinstance(history.updated_fields, str):
			history.updated_fields = ast.literal_eval(history.updated_fields)

	returnVal['patientHistory'] = patientHistory

	list_of_hamd = hamd.objects.filter(details=patient_id, is_delete=0)

	returnVal['list_of_hamd'] = [{"pk": hamd.pk, "consultation_date": hamd.consultation_date, "score": int(hamd.calculate_score()), "total_score": int(hamd.total_score)} for hamd in list_of_hamd]

	returnVal['list_of_encounter'] = encounter.objects.filter(details=patient_id, is_delete=0).order_by('-consultation_date')
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

	new_global_psychotrauma_screen.physical_violence = request.POST.get('physical_violence') or None
	new_global_psychotrauma_screen.sexual_violence = request.POST.get('sexual_violence') or None
	new_global_psychotrauma_screen.emotional_abuse = request.POST.get('emotional_abuse') or None
	new_global_psychotrauma_screen.serious_injury = request.POST.get('serious_injury') or None
	new_global_psychotrauma_screen.life_threatening = request.POST.get('life_threatening') or None
	
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

	new_considering_event.score_1_16 = sum(
		1 for i in list(range(1, 17)) + [18]
		if request.POST.get(f'considering_event_{i}') == 'Yes'
	)
	new_considering_event.total_score = sum(1 for i in range(1, 23) if request.POST.get(f'considering_event_{i}') == 'Yes')

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
	if current_id != "0":
		try:
			gps_details = global_psychotrauma_screen.objects.get(pk=current_id)
		except:
			returnVal['error_msg'] = "id does not exists"
			return JsonResponse(returnVal, safe=False)
		
		gps_details.consultation_date = formatDate(request.POST['consultation_date'])
		gps_details.event_description = request.POST['event_description']
		gps_details.event_happened = request.POST['event_happened']

		gps_details.physical_violence = request.POST.get('physical_violence', 'to yourself')
		gps_details.sexual_violence = request.POST.get('sexual_violence', 'to yourself')
		gps_details.emotional_abuse = request.POST.get('emotional_abuse', 'to yourself')
		gps_details.serious_injury = request.POST.get('serious_injury', 'to yourself')
		gps_details.life_threatening = request.POST.get('life_threatening', 'to yourself')
		
		gps_details.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False) == 'True'
		gps_details.cause_harm_to_others = request.POST.get('cause_harm_to_others', False) == 'True'
		gps_details.covid =  request.POST.get('covid', False) == 'True'
		gps_details.single_event_occurring = request.POST['single_event_occurring']
		gps_details.range_event_occurring_from = request.POST['range_event_occurring_from']
		gps_details.range_event_occurring_to = request.POST['range_event_occurring_to']
		try:
			gps_details.save()
		except Exception as e:
			print(f"Error saving GPS details: {str(e)}")
			returnVal['error_msg'] = f"Error on saving gps: {str(e)}"
			return JsonResponse(returnVal, safe=False)

		considering_event_details = considering_event.objects.get(global_psychotrauma_screen=gps_details.pk)
		considering_event_details.considering_event_1 = request.POST.get('considering_event_1', 'No')
		considering_event_details.considering_event_2 = request.POST.get('considering_event_2', 'No')
		considering_event_details.considering_event_3 = request.POST.get('considering_event_3', 'No')
		considering_event_details.considering_event_4 = request.POST.get('considering_event_4', 'No')
		considering_event_details.considering_event_5 = request.POST.get('considering_event_5', 'No')
		considering_event_details.considering_event_6 = request.POST.get('considering_event_6', 'No')
		considering_event_details.considering_event_7 = request.POST.get('considering_event_7', 'No')
		considering_event_details.considering_event_8 = request.POST.get('considering_event_8', 'No')
		considering_event_details.considering_event_9 = request.POST.get('considering_event_9', 'No')
		considering_event_details.considering_event_10 = request.POST.get('considering_event_10', 'No')
		considering_event_details.considering_event_11 = request.POST.get('considering_event_11', 'No')
		considering_event_details.considering_event_12 = request.POST.get('considering_event_12', 'No')
		considering_event_details.considering_event_13 = request.POST.get('considering_event_13', 'No')
		considering_event_details.considering_event_14 = request.POST.get('considering_event_14', 'No')
		considering_event_details.considering_event_15 = request.POST.get('considering_event_15', 'No')
		considering_event_details.considering_event_16 = request.POST.get('considering_event_16', 'No')
		considering_event_details.considering_event_17 = request.POST.get('considering_event_17', 'No')
		considering_event_details.considering_event_18 = request.POST.get('considering_event_18', 'No')
		considering_event_details.considering_event_19 = request.POST.get('considering_event_19', 'No')
		considering_event_details.considering_event_20 = request.POST.get('considering_event_20', 'No')
		considering_event_details.considering_event_21 = request.POST.get('considering_event_21', 'No')
		considering_event_details.considering_event_22 = request.POST.get('considering_event_22', 'No')
		considering_event_details.considering_event_23 = request.POST.get('considering_event_23', '1')

		considering_event_details.score_1_16 = sum(
			1 for i in list(range(1, 17)) + [18]
			if request.POST.get(f'considering_event_{i}') == 'Yes'
		)

		considering_event_details.total_score = sum(1 for i in range(1, 23) if request.POST.get(f'considering_event_{i}') == 'Yes')
		
		try:
			considering_event_details.save()
			returnVal['status_code'] = 1
		except Exception as e:
			returnVal['error_msg'] = f"Error on saving gps screen: {str(e)}"
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

		new_global_psychotrauma_screen.physical_violence = request.POST.get('physical_violence', 'to yourself')
		new_global_psychotrauma_screen.sexual_violence = request.POST.get('sexual_violence', 'to yourself')
		new_global_psychotrauma_screen.emotional_abuse = request.POST.get('emotional_abuse', 'to yourself')
		new_global_psychotrauma_screen.serious_injury = request.POST.get('serious_injury', 'to yourself')
		new_global_psychotrauma_screen.life_threatening = request.POST.get('life_threatening', 'to yourself')
		
		new_global_psychotrauma_screen.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False) == 'True'
		new_global_psychotrauma_screen.cause_harm_to_others = request.POST.get('cause_harm_to_others', False) == 'True'
		new_global_psychotrauma_screen.covid =  request.POST.get('covid', False) == 'True'
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
		new_considering_event.considering_event_1 = request.POST.get('considering_event_1', 'No')
		new_considering_event.considering_event_2 = request.POST.get('considering_event_2', 'No')
		new_considering_event.considering_event_3 = request.POST.get('considering_event_3', 'No')
		new_considering_event.considering_event_4 = request.POST.get('considering_event_4', 'No')
		new_considering_event.considering_event_5 = request.POST.get('considering_event_5', 'No')
		new_considering_event.considering_event_6 = request.POST.get('considering_event_6', 'No')
		new_considering_event.considering_event_7 = request.POST.get('considering_event_7', 'No')
		new_considering_event.considering_event_8 = request.POST.get('considering_event_8', 'No')
		new_considering_event.considering_event_9 = request.POST.get('considering_event_9', 'No')
		new_considering_event.considering_event_10 = request.POST.get('considering_event_10', 'No')
		new_considering_event.considering_event_11 = request.POST.get('considering_event_11', 'No')
		new_considering_event.considering_event_12 = request.POST.get('considering_event_12', 'No')
		new_considering_event.considering_event_13 = request.POST.get('considering_event_13', 'No')
		new_considering_event.considering_event_14 = request.POST.get('considering_event_14', 'No')
		new_considering_event.considering_event_15 = request.POST.get('considering_event_15', 'No')
		new_considering_event.considering_event_16 = request.POST.get('considering_event_16', 'No')
		new_considering_event.considering_event_17 = request.POST.get('considering_event_17', 'No')
		new_considering_event.considering_event_18 = request.POST.get('considering_event_18', 'No')
		new_considering_event.considering_event_19 = request.POST.get('considering_event_19', 'No')
		new_considering_event.considering_event_20 = request.POST.get('considering_event_20', 'No')
		new_considering_event.considering_event_21 = request.POST.get('considering_event_21', 'No')
		new_considering_event.considering_event_22 = request.POST.get('considering_event_22', 'No')
		new_considering_event.considering_event_23 = request.POST.get('considering_event_23', '1')

		considering_event_details.score_1_16 = sum(
			1 for i in list(range(1, 17)) + [18]
			if request.POST.get(f'considering_event_{i}') == 'Yes'
		)
		new_considering_event.total_score = sum(1 for i in range(1, 23) if request.POST.get(f'considering_event_{i}') == 'Yes')

		try:
			new_considering_event.save()
			returnVal['status_code'] = 1
		except Exception as e:
			new_global_psychotrauma_screen.delete()
			returnVal['error_msg'] = f"Error saving GPS screen: {str(e)}"
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
			returnVal['status_code'] = 1
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
			returnVal['status_code'] = 1
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

		global_psychotrauma_screen_instance.physical_violence = request.POST.get('physical_violence') or None
		global_psychotrauma_screen_instance.sexual_violence = request.POST.get('sexual_violence') or None
		global_psychotrauma_screen_instance.emotional_abuse = request.POST.get('emotional_abuse') or None
		global_psychotrauma_screen_instance.serious_injury = request.POST.get('serious_injury') or None
		global_psychotrauma_screen_instance.life_threatening = request.POST.get('life_threatening') or None

		global_psychotrauma_screen_instance.sudden_death_of_loved_one = request.POST.get('sudden_death_of_loved_one', False)
		global_psychotrauma_screen_instance.cause_harm_to_others = request.POST.get('cause_harm_to_others', False)
		global_psychotrauma_screen_instance.covid =  request.POST.get('covid', False)
		global_psychotrauma_screen_instance.single_event_occurring = request.POST['single_event_occurring']
		global_psychotrauma_screen_instance.range_event_occurring_from = request.POST['range_event_occurring_from']
		global_psychotrauma_screen_instance.range_event_occurring_to = request.POST['range_event_occurring_to']
		try:
			global_psychotrauma_screen_instance.save()
		except Exception as e:
			# returnVal['error_msg'] = f"Error on Saving the GPS Data: {str(e)}"
			returnVal['error_msg'] = f"Error on Saving the GPS Data"
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

		considering_event_instance.score_1_16 = sum(
			1 for i in list(range(1, 17)) + [18]
			if request.POST.get(f'considering_event_{i}') == 'Yes'
		)
		considering_event_instance.total_score = sum(1 for i in range(1, 23) if request.POST.get(f'considering_event_{i}') == 'Yes')

		try:
			considering_event_instance.save()
		except:
			returnVal['error_msg'] = "error on Saving the GPS Data!"
			return render(request, 'patient_edit_gps.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_edit_gps.html', returnVal)

@login_required(login_url='/login')
def PatientDeleteGPS(request, gps_id):
    """
    Soft delete a GPS record by setting is_delete=1, then redirect to the patient detail page.
    """
    try:
        gps_instance = global_psychotrauma_screen.objects.get(pk=gps_id)
        gps_instance.is_delete = 1
        gps_instance.save()
        patient_id = gps_instance.details.pk
        return redirect('PatientDetailed', patient_id=patient_id)
    except global_psychotrauma_screen.DoesNotExist:
        return HttpResponse('GPS record does not exist.', status=404)


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

		new_hamd.depersonalization_and_derelization = request.POST.get('depersonalization_and_derelization', False)
		total_score = total_score + int(new_hamd.depersonalization_and_derelization)
		new_hamd.paranoid_symptoms = request.POST.get('paranoid_symptoms', False)
		total_score = total_score + int(new_hamd.paranoid_symptoms)
		new_hamd.obsessional_symptoms = request.POST.get('obsessional_symptoms', False)
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
def PatientDeleteHamD(request, hamd_id):
    """
    Soft delete a HAMD record by setting is_delete=1, then redirect to the patient detail page.
    """
    try:
        hamd_instance = hamd.objects.get(pk=hamd_id)
        hamd_instance.is_delete = 1
        hamd_instance.save()
        patient_id = hamd_instance.details.pk
        return redirect('PatientDetailed', patient_id=patient_id)
    except hamd.DoesNotExist:
        return HttpResponse('HAMD record does not exist.', status=404)

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
	returnVal = {}
	referralDetails = Referral.objects.get(pk=referral_id)
	returnVal['referral_details'] = referralDetails
	encounter_details = encounter.objects.get(pk=referralDetails.encounter_id)
	returnVal['referral_diagnosis'] = diagnosis.objects.filter(encounter_id=referralDetails.encounter_id, is_delete=0)
	returnVal['referral_treatment'] = treatment.objects.filter(encounter_id=referralDetails.encounter_id, is_delete=0)
	returnVal['referral_history_present_illness'] = history_present_illness.objects.filter(encounter_id=referralDetails.encounter_id, is_delete=0)


	return render(request, 'referral_form.html', returnVal)


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


# ICF (Informed Consent Form) related functions
def get_icf_file_path(patient_id):
	"""Get the ICF file path for a patient using pattern matching"""
	import os
	import glob
	from django.conf import settings
	
	icf_dir = os.path.join(settings.MEDIA_ROOT, 'informed_consent')
	
	# Search for files matching the pattern *_ICF_patient_PATIENTID.pdf
	pattern = os.path.join(icf_dir, f"*_ICF_patient_{patient_id}.pdf")
	matching_files = glob.glob(pattern)
	
	if matching_files:
		# Return the first matching file (should only be one)
		return matching_files[0]
	else:
		# Return the expected path based on patient full name for new uploads
		try:
			patient_details = details.objects.get(pk=patient_id)
			last_name = patient_details.last_name.upper().replace(' ', '_')
			first_name = patient_details.first_name.upper().replace(' ', '_')
			middle_name = patient_details.middle_name.upper().replace(' ', '_') if patient_details.middle_name else ''
			
			if middle_name:
				filename = f"{last_name}_{first_name}_{middle_name}_ICF_patient_{patient_id}.pdf"
			else:
				filename = f"{last_name}_{first_name}_ICF_patient_{patient_id}.pdf"
			return os.path.join(icf_dir, filename)
		except details.DoesNotExist:
			# Fallback to old naming format
			filename = f"ICF_patient_{patient_id}.pdf"
			return os.path.join(icf_dir, filename)

def has_icf_file(patient_id):
	"""Check if ICF file exists for a patient using pattern matching"""
	import os
	import glob
	from django.conf import settings
	
	icf_dir = os.path.join(settings.MEDIA_ROOT, 'informed_consent')
	
	# Search for files matching the pattern *_ICF_patient_PATIENTID.pdf
	pattern = os.path.join(icf_dir, f"*_ICF_patient_{patient_id}.pdf")
	matching_files = glob.glob(pattern)
	
	return len(matching_files) > 0

@login_required(login_url='/login')
def CheckICFStatus(request, patient_id):
	"""Check ICF status for a patient via AJAX"""
	try:
		# Check both file system and database record
		has_file = has_icf_file(patient_id)
		
		# Also check if database record exists
		has_db_record = False
		try:
			patient_details = details.objects.get(pk=patient_id)
			has_db_record = details_files.objects.filter(
				details=patient_details,
				file_name__regex=r'.*_ICF_patient_' + str(patient_id) + r'\.pdf$',
				is_delete=False
			).exists()
		except details.DoesNotExist:
			pass
		
		# Return true if either file exists or database record exists
		has_icf = has_file or has_db_record
		
		return JsonResponse({
			'has_icf': has_icf,
			'has_file': has_file,
			'has_db_record': has_db_record
		})
	except Exception as e:
		return JsonResponse({'has_icf': False, 'error': str(e)})

@login_required(login_url='/login')
def UploadICF(request):
	"""Upload ICF file for a patient"""
	if request.method == 'POST':
		patient_id = request.POST.get('patient_id')
		icf_file = request.FILES.get('icf_file')
		
		if not patient_id or not icf_file:
			return JsonResponse({'error': 'Missing patient ID or file'}, status=400)
		
		# Validate file type
		if not icf_file.name.lower().endswith('.pdf'):
			return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)
		
		# Validate file size (5MB limit)
		if icf_file.size > 5 * 1024 * 1024:
			return JsonResponse({'error': 'File size cannot exceed 5MB'}, status=400)
		
		try:
			import os
			from django.conf import settings
			
			# Get patient details to use full name in filename
			patient_details = details.objects.get(pk=patient_id)
			last_name = patient_details.last_name.upper().replace(' ', '_')
			first_name = patient_details.first_name.upper().replace(' ', '_')
			middle_name = patient_details.middle_name.upper().replace(' ', '_') if patient_details.middle_name else ''
			
			# Create directory if it doesn't exist
			icf_dir = os.path.join(settings.MEDIA_ROOT, 'informed_consent')
			os.makedirs(icf_dir, exist_ok=True)
			
			# Save file with new naming format: LASTNAME_FIRSTNAME_MIDDLENAME_ICF_patient_PATIENTID
			if middle_name:
				filename = f"{last_name}_{first_name}_{middle_name}_ICF_patient_{patient_id}.pdf"
			else:
				filename = f"{last_name}_{first_name}_ICF_patient_{patient_id}.pdf"
			file_path = os.path.join(icf_dir, filename)
			
			# Remove existing ICF files if they exist (using pattern matching)
			import glob
			existing_files_pattern = os.path.join(icf_dir, f"*_ICF_patient_{patient_id}.pdf")
			existing_files = glob.glob(existing_files_pattern)
			for existing_file in existing_files:
				if os.path.exists(existing_file):
					os.remove(existing_file)
			
			# Save new file
			with open(file_path, 'wb+') as destination:
				for chunk in icf_file.chunks():
					destination.write(chunk)
			
			# Create database record for the uploaded ICF file
			try:
				# Remove existing ICF record if it exists (using pattern matching)
				details_files.objects.filter(
					details=patient_details,
					file_name__regex=r'.*_ICF_patient_' + str(patient_id) + r'\.pdf$'
				).delete()
				
				# Create new ICF record in details_files table
				details_files.objects.create(
					details=patient_details,
					file_name=filename,
					file=f'informed_consent/{filename}',  # Relative path from MEDIA_ROOT
					history=f'ICF uploaded by {request.user.username} on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
					status=True,
					is_delete=False
				)
				
			except details.DoesNotExist:
				return JsonResponse({'error': 'Patient not found'}, status=404)
			except Exception as db_error:
				# Log the database error but don't fail the upload since file was saved
				print(f"Database error while saving ICF record: {str(db_error)}")
			
			return redirect('PatientDetailed', patient_id=patient_id)
			
		except Exception as e:
			return JsonResponse({'error': f'Error uploading file: {str(e)}'}, status=500)
	
	return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required(login_url='/login')
def PreviewICF(request, patient_id):
	"""Preview ICF file for a patient"""
	import os
	from django.http import FileResponse, Http404
	
	file_path = get_icf_file_path(patient_id)
	
	if not os.path.exists(file_path):
		raise Http404("ICF file not found")
	
	try:
		# Get the actual filename from the file path
		actual_filename = os.path.basename(file_path)
		
		response = FileResponse(
			open(file_path, 'rb'),
			content_type='application/pdf'
		)
		response['Content-Disposition'] = f'inline; filename="{actual_filename}"'
		return response
	except Exception as e:
		raise Http404(f"Error loading file: {str(e)}")

@login_required(login_url='/login')
def DeleteICF(request, patient_id):
	"""Delete ICF file for a patient"""
	import os
	import glob
	from django.conf import settings
	
	# Delete all ICF files matching the pattern
	icf_dir = os.path.join(settings.MEDIA_ROOT, 'informed_consent')
	pattern = os.path.join(icf_dir, f"*_ICF_patient_{patient_id}.pdf")
	matching_files = glob.glob(pattern)
	
	for file_path in matching_files:
		if os.path.exists(file_path):
			try:
				os.remove(file_path)
			except Exception as e:
				return JsonResponse({'error': f'Error deleting file: {str(e)}'}, status=500)
	
	# Remove database record for the ICF file
	try:
		patient_details = details.objects.get(pk=patient_id)
		details_files.objects.filter(
			details=patient_details,
			file_name__regex=r'.*_ICF_patient_' + str(patient_id) + r'\.pdf$'
		).delete()
	except details.DoesNotExist:
		pass  # Patient not found, but file was already deleted
	except Exception as db_error:
		# Log the database error but don't fail the deletion
		print(f"Database error while deleting ICF record: {str(db_error)}")
	
	return redirect('PatientDetailed', patient_id=patient_id)
	
def serialize_value(value):
	if isinstance(value, (datetime, date)):
		return value.isoformat()
	return value