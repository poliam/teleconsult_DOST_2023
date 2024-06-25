from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from patient.models import details, relatives, medicine, allergies, global_psychotrauma_screen, hamd
from consultation.models import *
from consultation.consultation_form import AddConsultationVitalSignForm, AddConsultationEncounterForm, AddConsultationChiefComplaintForm, AddMentalGeneralDescriptionForm, AddMentalEmotionForm, AddMentalCognitiveForm, AddMentalThoughtPerceptionForm, AddMentalSuicidalityForm, AddReferralForm, patientNurseNotesForm
import random, os
from datetime import date, datetime

@login_required(login_url='/login')
def CreateConsultation(request, patient_id):
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
	returnVal['sidebar'] = "Consultation"
	returnVal['userDetails'] = profile_details
	try:
		patient_instance = details.objects.get(pk=patient_id)
	except:
		returnVal['error_msg'] = "Patient Does not exists"
		return render(request, 'error_page.html', returnVal)

	try:
		global_psychotrauma_screen_details = global_psychotrauma_screen.objects.get(details=patient_instance.pk)
		returnVal['global_psychotrauma_screen_details'] = global_psychotrauma_screen_details
	except:
		returnVal['global_psychotrauma_screen_details'] = False

	try:
		hamd_details = hamd.objects.get(details=patient_instance.pk)
		returnVal['hamd_details'] = hamd_details

	except:
		returnVal['hamd_details'] = False

	returnVal['vitalSignForm'] = AddConsultationVitalSignForm()
	returnVal['consultationEncounterForm'] = AddConsultationEncounterForm()
	returnVal['ConsultationChiefComplaintForm'] = AddConsultationChiefComplaintForm()
	returnVal['MentalGeneralDescriptionForm'] = AddMentalGeneralDescriptionForm()
	returnVal['MentalEmotionForm'] = AddMentalEmotionForm()
	returnVal['MentalCognitiveForm'] = AddMentalCognitiveForm()
	returnVal['MentalThoughtPerceptionForm'] = AddMentalThoughtPerceptionForm()
	returnVal['MentalSuicidalityForm'] = AddMentalSuicidalityForm()
	returnVal['ReferralForm'] = AddReferralForm()
	returnVal['condition_list'] = condition.objects.all()
	returnVal['medicine'] = medicine.objects.filter(is_delete=0, status=1)

	if request.method == 'POST':

		vitalSignForm = AddConsultationVitalSignForm(request.POST)
		returnVal['vitalSignForm'] = vitalSignForm
		consultationEncounterForm = AddConsultationEncounterForm(request.POST)
		returnVal['consultationEncounterForm'] = consultationEncounterForm
		ConsultationChiefComplaintForm = AddConsultationChiefComplaintForm(request.POST)
		returnVal['ConsultationChiefComplaintForm'] = ConsultationChiefComplaintForm
		MentalGeneralDescriptionForm = AddMentalGeneralDescriptionForm(request.POST)
		returnVal['MentalGeneralDescriptionForm'] = MentalGeneralDescriptionForm
		MentalEmotionForm = AddMentalEmotionForm(request.POST)
		returnVal['MentalEmotionForm'] = MentalEmotionForm
		MentalCognitiveForm = AddMentalCognitiveForm(request.POST)
		returnVal['MentalCognitiveForm'] = MentalCognitiveForm
		MentalThoughtPerceptionForm = AddMentalThoughtPerceptionForm(request.POST)
		returnVal['MentalThoughtPerceptionForm'] = MentalThoughtPerceptionForm
		MentalSuicidalityForm = AddMentalSuicidalityForm(request.POST)
		returnVal['MentalSuicidalityForm'] = MentalSuicidalityForm
		ReferralForm = AddReferralForm(request.POST)
		returnVal['ReferralForm'] = ReferralForm


		HOPI_List = []
		HOPI_NUM = request.POST.getlist('HOPI_NUM[]')
		HOPI_TIME = request.POST.getlist('HOPI_TIME[]')
		HOPI_DETAILS = request.POST.getlist('HOPI_DETAILS[]')
		for i in range(len(HOPI_NUM)):
			if HOPI_NUM[i] != "" or HOPI_TIME[i] != "" or HOPI_DETAILS[i] != "":
				HOPI_List.append({"HOPI_NUM":HOPI_NUM[i],"HOPI_TIME":HOPI_TIME[i],"HOPI_DETAILS":HOPI_DETAILS[i]})
		returnVal['HOPI_List'] = HOPI_List


		Condition_Form_list = []
		condition_val = request.POST.getlist('condition[]')
		condition_detail_val = request.POST.getlist('condition_detail[]')
		for i in range(len(condition_val)):
			if condition_val[i] != "" or condition_detail_val[i] != "":
				Condition_Form_list.append({"condition":condition_val[i], "condition_detail":condition_detail_val[i]})
		returnVal['conditionFormList'] = Condition_Form_list

		Treatment_form_list = []
		drug = request.POST.getlist('drug[]')
		strength = request.POST.getlist('strength[]')
		dose = request.POST.getlist('dose[]')
		Route = request.POST.getlist('Route[]')
		frequency = request.POST.getlist('frequency[]')
		drug_no = request.POST.getlist('drug_no[]')
		for i in range(len(drug)):
			if drug[i] != "":
				Treatment_form_list.append({'drug':drug, 'strength':strength, "dose":dose, "Route":Route, "frequency":frequency, "drug_no":drug_no})
		returnVal['treatmentFormList'] = Treatment_form_list



		if vitalSignForm.is_valid() and consultationEncounterForm.is_valid() and ConsultationChiefComplaintForm.is_valid() and MentalGeneralDescriptionForm.is_valid() and MentalEmotionForm.is_valid() and MentalCognitiveForm.is_valid() and MentalThoughtPerceptionForm.is_valid() and MentalSuicidalityForm.is_valid() and ReferralForm.is_valid():
			EncounterPost = consultationEncounterForm.save(commit=False)
			EncounterPost.details = patient_instance
			EncounterPost.consulted_by = profile_details
			EncounterPost.save()

			vitalSignPost = vitalSignForm.save(commit=False)
			vitalSignPost.encounter = EncounterPost
			vitalSignPost.save()

			ConsultationChiefComplaintPost = ConsultationChiefComplaintForm.save(commit=False)
			ConsultationChiefComplaintPost.encounter = EncounterPost
			ConsultationChiefComplaintPost.save()

			MentalGeneralDescriptionPost = MentalGeneralDescriptionForm.save(commit=False)
			MentalGeneralDescriptionPost.encounter =  EncounterPost
			MentalGeneralDescriptionPost.save()

			MentalEmotionPost = MentalEmotionForm.save(commit=False)
			MentalEmotionPost.encounter = EncounterPost
			MentalEmotionPost.save()

			MentalCognitivePost = MentalCognitiveForm.save(commit=False)
			MentalCognitivePost.encounter = EncounterPost
			MentalCognitivePost.save()

			MentalThoughtPerceptionPost = MentalThoughtPerceptionForm.save(commit=False)
			MentalThoughtPerceptionPost.encounter = EncounterPost
			MentalThoughtPerceptionPost.save()

			MentalSuicidalityPost = MentalSuicidalityForm.save(commit=False)
			MentalSuicidalityPost.encounter = EncounterPost
			MentalSuicidalityPost.save()

			referred_to = request.POST.get('referred_to', False)
			impression = request.POST.get('impression', False)
			reason_for_referral = request.POST.get('reason_for_referral', False)



			if referred_to != "" and impression !="" and reason_for_referral != "":
				ReferralFormPost = ReferralForm.save(commit=False)
				ReferralFormPost.encounter = EncounterPost
				ReferralFormPost.save()

			for i in range(len(HOPI_NUM)):
				if HOPI_NUM[i] != "" or HOPI_TIME[i] != "" or HOPI_DETAILS[i] != "":
					new_history_present_illness = history_present_illness()
					new_history_present_illness.number = HOPI_NUM[i]
					new_history_present_illness.calendrical = HOPI_TIME[i]
					new_history_present_illness.details = HOPI_DETAILS[i]
					new_history_present_illness.encounter = EncounterPost
					new_history_present_illness.save()

			for i in range(len(condition_val)):
				if condition_val[i] != "" or condition_detail_val[i] != "":
					try:
						condition_instance = condition.objects.get(name=condition_val[i])
					except:
						new_condition = condition()
						new_condition.name = condition_val[i]
						new_condition.save()
						condition_instance = new_condition
					new_diagnosis = diagnosis()
					new_diagnosis.condition = condition_instance
					new_diagnosis.condition_details = condition_detail_val[i]
					new_diagnosis.encounter = EncounterPost
					new_diagnosis.save()

			for i in range(len(drug)):
				if drug[i] != "":
					try:
						medicine_instance = medicine.objects.get(name=drug[i])
					except:
						new_medicine = medicine()
						new_medicine.name = drug[i]
						new_medicine.save()
						medicine_instance = new_medicine
					new_treatment = treatment()
					new_treatment.drugs = medicine_instance
					new_treatment.strength = strength[i]
					new_treatment.dose = dose[i]
					new_treatment.route = Route[i]
					new_treatment.frequency = frequency[i]
					new_treatment.drug_no = drug_no[i]
					new_treatment.encounter = EncounterPost
					new_treatment.save()
			return redirect("PatientDetailed", patient_id=patient_instance.pk)

		else:
			return render(request, 'consultation_create.html', returnVal)
	
	returnVal['patientDetailed'] = patient_instance
	return render(request, 'consultation_create.html', returnVal)

@login_required(login_url='/login')
def EncounterDetails(request):
	returnVal = {}
	encounter_id = request.GET['enouter_id']


	returnVal['encounter_details'] = encounter.objects.get(pk=encounter_id)
	try:
		returnVal['vital_sign'] = vitalsign.objects.get(encounter=encounter_id)
	except:
		returnVal['vital_sign'] = ""
	try:
		returnVal['chief_complaints'] = chief_complaints.objects.get(encounter=encounter_id)
	except:
		returnVal['chief_complaints'] = ""
	try:
		returnVal['history_present_illness'] = history_present_illness.objects.filter(encounter=encounter_id, is_delete=0, status=1)
	except:
		returnVal['history_present_illness'] = ""

	try:
		returnVal['mental_general_description'] = mental_general_description.objects.get(encounter=encounter_id)
	except:
		returnVal['mental_general_description'] = ""

	try:
		returnVal['mental_emotions'] =  mental_emotions.objects.get(encounter=encounter_id)
	except:
		returnVal['mental_emotions'] = ""

	try:	
		returnVal['mental_cognitive_function'] = mental_cognitive_function.objects.get(encounter=encounter_id)
	except:
		returnVal['mental_cognitive_function'] = ""
	try:	
		returnVal['mental_thought_perception'] = mental_thought_perception.objects.get(encounter=encounter_id)
	except:
		returnVal['mental_thought_perception'] = ""
	try:
		returnVal['referral_details'] = Referral.objects.get(encounter=encounter_id)
	except:
		returnVal['referral_details'] = ""

	try:
		returnVal['suicidality'] = suicidality.objects.get(encounter=encounter_id)
	except:
		returnVal['suicidality'] = ""
	try:
		returnVal['diagnosis_list'] = diagnosis.objects.filter(encounter=encounter_id, is_delete=0, status=1)
	except:
		returnVal['diagnosis_list'] = ""

	try:
		returnVal['drug_list'] = treatment.objects.filter(encounter=encounter_id, is_delete=0, status=1)
	except:
		returnVal['drug_list'] = ""

	returnVal['list_of_nurse_notes'] = nurse_notes.objects.filter(encounter=encounter_id)

	
	html = render_to_string('consultation_details.html', returnVal)
	return HttpResponse(html)

@login_required(login_url='login')
def EditConsultation(request, encounter_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "Consultation"
	returnVal['userDetails'] = profile_details
	if request.user.groups.filter(name="Doctor").exists():
		returnVal['group_type'] = "Doctor"
	elif request.user.groups.filter(name="Nurse").exists():
		returnVal['group_type'] = "Nurse"
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Triage"
	elif request.user.groups.filter(name="Admin").exists():
		returnVal['group_type'] = "Admin"

		
	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
		returnVal['encounter_details'] = encounter_instance
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return render(request, 'error_page.html', returnVal)

	try:
		patient_instance = details.objects.get(pk=encounter_instance.details.pk)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return render(request, 'error_page.html', returnVal)

	try:
		vitalsign_instance = vitalsign.objects.get(encounter=encounter_id)
		returnVal['vitalSignForm'] = AddConsultationVitalSignForm(instance=vitalsign_instance)
	except:
		returnVal['vitalSignForm'] = AddConsultationVitalSignForm()


	returnVal['consultationEncounterForm'] = AddConsultationEncounterForm(instance=encounter_instance)

	try:
		chief_complaints_instance = chief_complaints.objects.get(encounter=encounter_id)
		returnVal['ConsultationChiefComplaintForm'] = AddConsultationChiefComplaintForm(instance=chief_complaints_instance)
	except:
		returnVal['ConsultationChiefComplaintForm'] = AddConsultationChiefComplaintForm()

	try:
		mental_general_description_instance = mental_general_description.objects.get(encounter=encounter_id)
		returnVal['MentalGeneralDescriptionForm'] = AddMentalGeneralDescriptionForm(instance=mental_general_description_instance)
	except:
		returnVal['MentalGeneralDescriptionForm'] = AddMentalGeneralDescriptionForm()

	try:
		mental_emotions_instance = mental_emotions.objects.get(encounter=encounter_id)
		returnVal['MentalEmotionForm'] = AddMentalEmotionForm(instance=mental_emotions_instance)
	except:
		returnVal['MentalEmotionForm'] = AddMentalEmotionForm()

	try:
		mental_cognitive_function_instance = mental_cognitive_function.objects.get(encounter=encounter_id)
		returnVal['MentalCognitiveForm'] = AddMentalCognitiveForm(instance=mental_cognitive_function_instance)
	except:
		returnVal['MentalCognitiveForm'] = AddMentalCognitiveForm()

	try:
		mental_thought_perception_instance = mental_thought_perception.objects.get(encounter=encounter_id)
		returnVal['MentalThoughtPerceptionForm'] = AddMentalThoughtPerceptionForm(instance=mental_thought_perception_instance)
	except:
		returnVal['MentalThoughtPerceptionForm'] = AddMentalThoughtPerceptionForm()

	try:
		suicidality_instance = suicidality.objects.get(encounter=encounter_id)
		returnVal['MentalSuicidalityForm'] = AddMentalSuicidalityForm(instance=suicidality_instance)
	except:
		returnVal['MentalSuicidalityForm'] = AddMentalSuicidalityForm()


	try:
		Referral_instance = Referral.objects.get(encounter=encounter_id)
		returnVal['ReferralForm'] = AddReferralForm(instance=Referral_instance)
	except:
		returnVal['ReferralForm'] = AddReferralForm()

	try:
		treatment_list = treatment.objects.filter(encounter=encounter_id, is_delete=0, status=1)
		returnVal['treatment_list'] = treatment_list
	except:
		returnVal['treatment_list'] = False

	try:
		global_psychotrauma_screen_details = global_psychotrauma_screen.objects.get(details=patient_instance.pk)
		returnVal['global_psychotrauma_screen_details'] = global_psychotrauma_screen_details
	except:
		returnVal['global_psychotrauma_screen_details'] = False

	try:
		hamd_details = hamd.objects.get(details=patient_instance.pk)

		returnVal['hamd_details'] = hamd_details
	except:
		returnVal['hamd_details'] = False
	returnVal['patientNurseNotesForm'] = patientNurseNotesForm()

	returnVal['list_of_nurse_notes'] = nurse_notes.objects.filter(encounter=encounter_id)



	if request.method == 'POST':
		try:
			vitalsign_instance = vitalsign.objects.get(encounter=encounter_id)
			vitalSignForm = AddConsultationVitalSignForm(request.POST, instance=vitalsign_instance)
		except:
			vitalSignForm = AddConsultationVitalSignForm(request.POST)
		returnVal['vitalSignForm'] = vitalSignForm
		
		consultationEncounterForm = AddConsultationEncounterForm(request.POST, instance=encounter_instance)
		returnVal['consultationEncounterForm'] = consultationEncounterForm
		
		try:
			chief_complaints_instance = chief_complaints.objects.get(encounter=encounter_id)
			ConsultationChiefComplaintForm = AddConsultationChiefComplaintForm(request.POST, instance=chief_complaints_instance)
		except:
			ConsultationChiefComplaintForm = AddConsultationChiefComplaintForm(request.POST)
		returnVal['ConsultationChiefComplaintForm'] = ConsultationChiefComplaintForm
		
		try:
			mental_general_description_instance = mental_general_description.objects.get(encounter=encounter_id)
			MentalGeneralDescriptionForm = AddMentalGeneralDescriptionForm(request.POST, instance=mental_general_description_instance)
		except:
			MentalGeneralDescriptionForm = AddMentalGeneralDescriptionForm(request.POST)
			returnVal['MentalGeneralDescriptionForm'] = MentalGeneralDescriptionForm

		try:
			mental_emotions_instance = mental_emotions.objects.get(encounter=encounter_id)
			MentalEmotionForm = AddMentalEmotionForm(request.POST, instance=mental_emotions_instance)
		except:
			MentalEmotionForm = AddMentalEmotionForm(request.POST)
		returnVal['MentalEmotionForm'] = MentalEmotionForm

		try:
			mental_cognitive_function_instance = mental_cognitive_function.objects.get(encounter=encounter_id)
			MentalCognitiveForm = AddMentalCognitiveForm(request.POST, instance=mental_cognitive_function_instance)
		except:
			MentalCognitiveForm = AddMentalCognitiveForm(request.POST)
		returnVal['MentalCognitiveForm'] = MentalCognitiveForm

		try:
			mental_thought_perception_instance = mental_thought_perception.objects.get(encounter=encounter_id)
			MentalThoughtPerceptionForm = AddMentalThoughtPerceptionForm(request.POST, instance=mental_thought_perception_instance)
		except:
			MentalThoughtPerceptionForm = AddMentalThoughtPerceptionForm(request.POST)
		returnVal['MentalThoughtPerceptionForm'] = MentalThoughtPerceptionForm

		try:
			suicidality_instance = suicidality.objects.get(encounter=encounter_id)
			MentalSuicidalityForm = AddMentalSuicidalityForm(request.POST, instance=suicidality_instance)
		except:
			MentalSuicidalityForm = AddMentalSuicidalityForm(request.POST)
		returnVal['MentalSuicidalityForm'] = MentalSuicidalityForm

		try:
			Referral_instance = Referral.objects.get(encounter=encounter_id)
			ReferralForm = AddReferralForm(request.POST, instance=Referral_instance)
		except:
			ReferralForm = AddReferralForm(request.POST)
		returnVal['ReferralForm'] = ReferralForm

		if vitalSignForm.is_valid() and consultationEncounterForm.is_valid() and ConsultationChiefComplaintForm.is_valid() and MentalGeneralDescriptionForm.is_valid() and MentalEmotionForm.is_valid() and MentalCognitiveForm.is_valid() and MentalThoughtPerceptionForm.is_valid() and MentalSuicidalityForm.is_valid() and ReferralForm.is_valid():
			EncounterPost = consultationEncounterForm.save(commit=False)
			EncounterPost.update_by = profile_details
			if returnVal['group_type'] == "Doctor":
				EncounterPost.consulted_by = profile_details
			EncounterPost.save()

			vitalSignPost = vitalSignForm.save(commit=False)
			vitalSignPost.encounter =  encounter_instance
			vitalSignPost.save()

			ConsultationChiefComplaintPost = ConsultationChiefComplaintForm.save(commit=False)
			ConsultationChiefComplaintPost.encounter =  encounter_instance
			ConsultationChiefComplaintPost.save()

			MentalGeneralDescriptionPost = MentalGeneralDescriptionForm.save(commit=False)
			MentalGeneralDescriptionPost.encounter =  encounter_instance
			MentalGeneralDescriptionPost.save()

			MentalEmotionPost = MentalEmotionForm.save(commit=False)
			MentalEmotionPost.encounter =  encounter_instance
			MentalEmotionPost.save()

			MentalCognitivePost = MentalCognitiveForm.save(commit=False)
			MentalCognitivePost.encounter =  encounter_instance
			MentalCognitivePost.save()

			MentalThoughtPerceptionPost = MentalThoughtPerceptionForm.save(commit=False)
			MentalThoughtPerceptionPost.encounter =  encounter_instance
			MentalThoughtPerceptionPost.save()

			MentalSuicidalityPost = MentalSuicidalityForm.save(commit=False)
			MentalSuicidalityPost.encounter =  encounter_instance
			MentalSuicidalityPost.save()

			referred_to = request.POST.get('referred_to', False)
			reason_for_referral = request.POST.get('reason_for_referral', False)

			if referred_to != "" and reason_for_referral != "":
				ReferralFormPost = ReferralForm.save(commit=False)
				ReferralFormPost.encounter =  encounter_instance
				ReferralFormPost.save()
				# Check which button was clicked
				if 'action' in request.POST:
					if request.POST.get('action') == 'update':
						# Process the data but stay on the same page
						returnVal['condition_list'] = condition.objects.all()
						returnVal['medicine'] = medicine.objects.filter(is_delete=0, status=1)
						returnVal['patientDetailed'] = patient_instance
						returnVal['history_present_illness_list'] = history_present_illness.objects.filter(encounter=encounter_id, is_delete=0, status=1)
						returnVal['diagnosis_list'] = diagnosis.objects.filter(encounter=encounter_id, is_delete=0, status=1)
						return render(request, 'consultation_edit.html', returnVal)
					elif request.POST.get('action') == 'save_exit':
						# Process the data and redirect
						# Example: Save the data and then redirect
						return redirect("PatientDetailed", patient_id=patient_instance.pk)
			else:
				if 'action' in request.POST:
					if request.POST.get('action') == 'update':
						# Process the data but stay on the same page
						returnVal['condition_list'] = condition.objects.all()
						returnVal['medicine'] = medicine.objects.filter(is_delete=0, status=1)
						returnVal['patientDetailed'] = patient_instance
						returnVal['history_present_illness_list'] = history_present_illness.objects.filter(encounter=encounter_id, is_delete=0, status=1)
						returnVal['diagnosis_list'] = diagnosis.objects.filter(encounter=encounter_id, is_delete=0, status=1)
						return render(request, 'consultation_edit.html', returnVal)
					elif request.POST.get('action') == 'save_exit':
						# Process the data and redirect
						# Example: Save the data and then redirect
						return redirect("PatientDetailed", patient_id=patient_instance.pk)


	
	returnVal['condition_list'] = condition.objects.all()
	returnVal['medicine'] = medicine.objects.filter(is_delete=0, status=1)
	returnVal['patientDetailed'] = patient_instance
	returnVal['history_present_illness_list'] = history_present_illness.objects.filter(encounter=encounter_id, is_delete=0, status=1)
	returnVal['diagnosis_list'] = diagnosis.objects.filter(encounter=encounter_id, is_delete=0, status=1)
	return render(request, 'consultation_edit.html', returnVal)

@login_required(login_url='login')
def CreateHOPI(request):
	returnVal = {}
	returnVal['status_code'] = 0
	encounter_id = request.POST['encounter_id']
	HOPI_NUM = request.POST['HOPI_NUM']
	HOPI_DETAILS = request.POST['HOPI_DETAILS']
	HOPI_TIME = request.POST['HOPI_TIME']
	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)

	new_history_present_illness = history_present_illness();
	new_history_present_illness.number = HOPI_NUM
	new_history_present_illness.calendrical = HOPI_TIME
	new_history_present_illness.details = HOPI_DETAILS
	new_history_present_illness.encounter = encounter_instance
	try:
		new_history_present_illness.save();
		returnVal['status_code'] = 1
		returnVal['HOPI_ID'] = new_history_present_illness.pk
	except:
		returnVal['error_msg'] = "Error on saving History of present illness"
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='login')
def DeleteHOPI(request):
	returnVal = {}
	returnVal['status_code'] = 0
	HOPI_id = request.POST['HOPI_ID']
	try:
		HOPI_instance = history_present_illness.objects.get(pk=HOPI_id)
	except:
		returnVal['error_msg'] = "History of present illness Does not exists"
		return JsonResponse(returnVal, safe=False)

	HOPI_instance.is_delete = 1
	HOPI_instance.status = 0
	try:
		HOPI_instance.save()
		returnVal['status_code'] = 1
	except:
		returnVal['error_msg'] = "Error on deleting History of present illness!"
		return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='login')
def AutoCreateHOPI(request):
	returnVal = {}
	returnVal['status_code'] = 0
	HOPI_ID = request.POST['HOPI_current_id']
	encounter_id = request.POST['HOPI_encounter_id']
	HOPI_NUM = request.POST['HOPI_NUM']
	HOPI_DETAILS = request.POST['HOPI_DETAILS']
	HOPI_TIME = request.POST['HOPI_TIME']
	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)
	if(HOPI_ID != "0"):
		try:
			current_history_present_illness = history_present_illness.objects.get(pk=HOPI_ID)
		except:
			returnVal['error_msg'] = "Error on getting present illness details"
			return JsonResponse(returnVal, safe=False)

		current_history_present_illness.number = HOPI_NUM
		current_history_present_illness.calendrical = HOPI_TIME
		current_history_present_illness.details = HOPI_DETAILS
		try:
			current_history_present_illness.save();
			returnVal['status_code'] = 1
			returnVal['HOPI_ID'] = HOPI_ID
		except:
			returnVal['error_msg'] = "Error on updating History of present illness"
	else:
		new_history_present_illness = history_present_illness();
		new_history_present_illness.number = HOPI_NUM
		new_history_present_illness.calendrical = HOPI_TIME
		new_history_present_illness.details = HOPI_DETAILS
		new_history_present_illness.encounter = encounter_instance
		try:
			new_history_present_illness.save();
			returnVal['status_code'] = 1
			returnVal['HOPI_ID'] = new_history_present_illness.pk
		except:
			returnVal['error_msg'] = "Error on saving History of present illness"

	return JsonResponse(returnVal, safe=False)


@login_required(login_url='login')
def CreateDiagnosis(request):
	returnVal = {}
	returnVal['status_code'] = 0
	encounter_id = request.POST['encounter_id']
	condition_name = request.POST['condition_name']
	condition_details = request.POST['condition_details']

	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)

	try:
		condition_instance = condition.objects.get(name=condition_name)
	except:
		new_condition = condition()
		new_condition.name = condition_name
		try:
			new_condition.save()
			condition_instance = new_condition
		except:
			returnVal['error_msg'] = "Error on Creating new condition"
			return JsonResponse(returnVal, safe=False)

	new_diagnosis = diagnosis()
	new_diagnosis.condition = condition_instance
	new_diagnosis.condition_details = condition_details
	new_diagnosis.encounter = encounter_instance
	try:
		new_diagnosis.save()
		returnVal['status_code'] = 1
		returnVal['diagnosis_id'] = new_diagnosis.pk
	except:
		returnVal['error_msg'] = "Error on saving Diagnosis!"
		return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='login')
def DeleteDiagnosis(request):
	returnVal = {}
	returnVal['status_code'] = 0
	diagnosis_id = request.POST['diagnosis_id']
	try:
		diagnosis_instance = diagnosis.objects.get(pk=diagnosis_id)
	except:
		returnVal['error_msg'] = "Diagnosis Does not exists"
		return JsonResponse(returnVal, safe=False)

	diagnosis_instance.is_delete = 1
	diagnosis_instance.status = 0
	try:
		diagnosis_instance.save()
		returnVal['status_code'] = 1
	except:
		returnVal['error_msg'] = "Error on deleting Diagnosis!"
		return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='login')
def CreateTreatment(request):
	returnVal = {}
	returnVal['status_code'] = 0
	encounter_id = request.POST['encounter_id']
	drug = request.POST['drug']
	strength = request.POST['strength']
	dose = request.POST['dose']
	Route = request.POST['Route']
	frequency = request.POST['frequency']
	no = request.POST['no']
	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)
	try:
		medicine_instance = medicine.objects.get(name=drug)
	except:
		new_medicine = medicine()
		new_medicine.name = drug
		try:
			new_medicine.save()
			medicine_instance = new_medicine
		except:
			returnVal['error_msg'] = "Error on saving medicine"
			return JsonResponse(returnVal, safe=False)

	new_treatment = treatment()
	new_treatment.drugs = medicine_instance
	new_treatment.strength = strength
	new_treatment.dose = dose
	new_treatment.route = Route
	new_treatment.frequency = frequency
	new_treatment.drug_no = no
	new_treatment.encounter = encounter_instance
	try:
		new_treatment.save()
		returnVal['status_code'] = 1
		returnVal['treatment_id'] = new_treatment.pk
	except:
		returnVal['error_msg'] = "Error on saving treatment"
		return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)

@login_required(login_url='login')
def DeleteTreatment(request):
	returnVal = {}
	returnVal['status_code'] = 0
	drug_id = request.POST['drug_id']
	try:
		treatment_instance = treatment.objects.get(pk=drug_id)
	except:
		returnVal['error_msg'] = "treatment Does not exists"
		return JsonResponse(returnVal, safe=False)

	treatment_instance.is_delete = 1
	treatment_instance.status = 0
	try:
		treatment_instance.save()
		returnVal['status_code'] = 1
	except:
		returnVal['error_msg'] = "Error on deleting treatment!"
		return JsonResponse(returnVal, safe=False)
	return JsonResponse(returnVal, safe=False)


@login_required(login_url='login')
def CreateNurseNotes(request):
	returnVal = {}
	returnVal['status_code'] = 0
	try:
		encounter_instance = encounter.objects.get(pk=request.POST['encounter_id'])
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)

	new_nurse_comment = nurse_notes()
	new_nurse_comment.comment = request.POST['comment']
	new_nurse_comment.create_by = request.user
	new_nurse_comment.encounter = encounter_instance

	try:
		new_nurse_comment.save()
		returnVal['status_code'] = 1
	except:
		returnVal['error_msg'] = "Error on creating comment"
		return JsonResponse(returnVal, safe=False)

	return JsonResponse(returnVal, safe=False)
	

@login_required(login_url='login')
def getNurseList(request):
	returnVal = {}
	encounter_id = request.GET['enouter_id']
	try:
		encounter_instance = encounter.objects.get(pk=encounter_id)
	except:
		returnVal['error_msg'] = "Encounter Does not exists"
		return JsonResponse(returnVal, safe=False)

	returnVal['list_of_nurse_notes'] = nurse_notes.objects.filter(encounter=encounter_id)
	html = render_to_string('consultation_nurse_notes.html', returnVal)
	return HttpResponse(html)

# Create your views here.
