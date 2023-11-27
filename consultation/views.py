from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from patient.models import details, relatives, medicine, allergies
from consultation.models import *
from consultation.consultation_form import AddConsultationVitalSignForm, AddConsultationEncounterForm, AddConsultationChiefComplaintForm, AddMentalGeneralDescriptionForm, AddMentalEmotionForm, AddMentalCognitiveForm, AddMentalThoughtPerceptionForm, AddMentalSuicidalityForm
import random, os
from datetime import date, datetime

@login_required(login_url='/login')
def CreateConsultation(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "Consultation"
	returnVal['userDetails'] = profile_details
	try:
		patient_instance = details.objects.get(pk=patient_id)
	except:
		returnVal['error_msg'] = "Patient Does not exists"
		return render(request, 'error_page.html', returnVal)

	returnVal['vitalSignForm'] = AddConsultationVitalSignForm()
	returnVal['consultationEncounterForm'] = AddConsultationEncounterForm()
	returnVal['ConsultationChiefComplaintForm'] = AddConsultationChiefComplaintForm()
	returnVal['MentalGeneralDescriptionForm'] = AddMentalGeneralDescriptionForm()
	returnVal['MentalEmotionForm'] = AddMentalEmotionForm()
	returnVal['MentalCognitiveForm'] = AddMentalCognitiveForm()
	returnVal['MentalThoughtPerceptionForm'] = AddMentalThoughtPerceptionForm()
	returnVal['MentalSuicidalityForm'] = AddMentalSuicidalityForm()
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



		if vitalSignForm.is_valid() and consultationEncounterForm.is_valid() and ConsultationChiefComplaintForm.is_valid() and MentalGeneralDescriptionForm.is_valid() and MentalEmotionForm.is_valid() and MentalCognitiveForm.is_valid() and MentalThoughtPerceptionForm.is_valid() and MentalSuicidalityForm.is_valid():
			EncounterPost = consultationEncounterForm.save(commit=False)
			EncounterPost.details = patient_instance
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

			for i in range(len(HOPI_NUM)):
				if HOPI_NUM[i] != "" or HOPI_TIME[i] != "" or HOPI_DETAILS[i] != "":
					new_history_present_illness = history_present_illness()
					new_history_present_illness.number = HOPI_NUM[i]
					new_history_present_illness.calendrical = HOPI_TIME[i]
					new_history_present_illness.details = HOPI_TIME[i]
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
	returnVal['chief_complaints'] = chief_complaints.objects.get(encounter=encounter_id)
	returnVal['history_present_illness'] = history_present_illness.objects.filter(encounter=encounter_id)
	returnVal['mental_general_description'] = mental_general_description.objects.get(encounter=encounter_id)
	html = render_to_string('consultation_details.html', returnVal)
	return HttpResponse(html)

# Create your views here.
