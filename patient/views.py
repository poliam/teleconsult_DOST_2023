from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from patient.models import details, address
import random, os
from datetime import date, datetime


@login_required(login_url='/login')
def PatientLists(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	list_of_patients = details.objects.filter(is_delete=0)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['list_of_patients'] = list_of_patients
	return render(request, 'patient_list.html', returnVal)

@login_required(login_url='/login')
def PatientCreate(request):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['error_msg'] = ""
	if request.method == 'POST':

		returnVal['Fname'] = request.POST['Fname']
		returnVal['Mname'] = request.POST['Mname']
		returnVal['Lname'] = request.POST['Lname']
		returnVal['gender'] = request.POST['gender']
		returnVal['birth_date'] = request.POST['birth_date']
		returnVal['marital_status'] = request.POST['marital_status']
		returnVal['contact_number'] = request.POST['contact_number']
		returnVal['alias'] = request.POST['alias']
		returnVal['Patient_email'] = request.POST['Patient_email']
		new_patient = details()
		new_patient.first_name = request.POST['Fname']
		new_patient.middle_name = request.POST['Mname']
		new_patient.last_name = request.POST['Lname']
		new_patient.gender = request.POST['gender']
		new_patient.BOD = formatDate(request.POST['birth_date'])
		new_patient.marital_status = request.POST['marital_status']
		new_patient.contact_number = request.POST['contact_number']
		new_patient.alias = request.POST['alias'] 
		new_patient.email = request.POST['Patient_email']
		
		returnVal['current_street_address'] = request.POST['current_street_address']
		returnVal['apt'] = request.POST['apt']
		returnVal['current_address_city'] = request.POST['current_address_city']
		returnVal['current_address_country'] = request.POST['current_address_country']
		returnVal['current_address_zipcode'] = request.POST['current_address_zipcode']

		current_address = address()
		current_address.street = request.POST['current_street_address']
		current_address.apt = request.POST['apt']
		current_address.city = request.POST['current_address_city']
		current_address.country = request.POST['current_address_country']
		current_address.zip_code = request.POST['current_address_zipcode']

		returnVal['ph_street_address'] = request.POST['ph_street_address']
		returnVal['ph_barangay'] = request.POST['ph_barangay']
		returnVal['province'] = request.POST['province']
		returnVal['ph_city'] = request.POST['ph_city']

		ph_address = address()
		ph_address.street = request.POST['ph_street_address']
		ph_address.barangay = request.POST['ph_barangay']
		ph_address.city = request.POST['ph_city']
		ph_address.country = "Philippines"
		ph_address.province = request.POST['province']
		ph_address.is_current = 0

		returnVal['birth_place'] = request.POST['birth_place']
		returnVal['religion'] = request.POST['religion']
		returnVal['highest_educational_attainment'] = request.POST['highest_educational_attainment']
		returnVal['citizenship'] = request.POST['citizenship']
		returnVal['Nationality'] = request.POST['Nationality']
		returnVal['Workplace'] = request.POST['Workplace']
		returnVal['Occupation'] = request.POST['Occupation']

		new_patient.birth_place = request.POST['birth_place']
		new_patient.religion = request.POST['religion']
		new_patient.high_education = request.POST['highest_educational_attainment']
		new_patient.citizenship = request.POST['citizenship']
		new_patient.nationality = request.POST['Nationality']
		new_patient.workplace = request.POST['Workplace'] 
		new_patient.occupation = request.POST['Occupation']

		if formatDate(request.POST['birth_date']) == False:
			returnVal['error_msg'] = "Date of Birth has format error!"
			return render(request, 'patient_create.html', returnVal)
		try:
			new_patient.save()
		except:
			returnVal['error_msg'] = "Error on Saving a Patient"
			return render(request, 'patient_create.html', returnVal)

		request_file = request.FILES['patientProf'] if 'patientProf' in request.FILES else None
		if request_file:
			split_tup = os.path.splitext(request_file.name)
			file_extension = split_tup[1]
			random_number = random.randint(0,1000)
			fs = FileSystemStorage()
			file_name = "prof_pic/profile_picture_"+str(request.user.id)+"_"+str(random_number)+""+str(file_extension)
			ProfPic = fs.save(file_name, request_file)
			new_patient.profile_picture = ProfPic
			try:
				new_patient.save()
			except:
				new_patient.delete()
				returnVal['error_msg'] = "Error on Saving a Patient Picture!"
				return render(request, 'patient_edit.html', returnVal)
		current_address.details = new_patient
		ph_address.details = new_patient
		try:
			current_address.save()
		except:
			new_patient.delete()
			returnVal['error_msg'] = "Error on Saving Current address!"
			return render(request, 'patient_create.html', returnVal)
		try:
			ph_address.save()
		except:
			current_address.delete()
			new_patient.delete()
			returnVal['error_msg'] = "Error on Saving PH address!"
			return render(request, 'patient_create.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_create.html', returnVal)

@login_required(login_url='/login')
def PatientDetailed(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	patient_instance = details.objects.get(pk=patient_id)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	returnVal['patientDetailed'] = patient_instance
	returnVal['age'] = datetime.now().year - 	patient_instance.BOD.year
	return render(request, 'patient_detailed.html', returnVal)

@login_required(login_url='/login')
def PatientEdit(request, patient_id):
	returnVal = {}
	profile_details = User.objects.get(pk=request.user.id)
	returnVal['sidebar'] = "patient"
	returnVal['userDetails'] = profile_details
	patient_instance = details.objects.get(pk=patient_id)
	current_address = address.objects.get(is_current=1, details=patient_instance)
	ph_address = address.objects.get(is_current=0, details=patient_instance)
	returnVal['patientDetailed'] = patient_instance
	returnVal['patientCurrentAddress'] = current_address
	returnVal['patientPhAddress'] = ph_address
	if request.method == 'POST':
		patient_instance.first_name = request.POST['Fname']
		patient_instance.middle_name = request.POST['Mname']
		patient_instance.last_name = request.POST['Lname']
		patient_instance.gender = request.POST['gender']
		patient_instance.BOD = formatDate(request.POST['birth_date'])
		patient_instance.marital_status = request.POST['marital_status']
		patient_instance.contact_number = request.POST['contact_number']
		patient_instance.alias = request.POST['alias'] 
		patient_instance.email = request.POST['Patient_email']
		patient_instance.birth_place = request.POST['birth_place']
		patient_instance.religion = request.POST['religion']
		patient_instance.high_education = request.POST['highest_educational_attainment']
		patient_instance.citizenship = request.POST['citizenship']
		patient_instance.nationality = request.POST['Nationality']
		patient_instance.workplace = request.POST['Workplace'] 
		patient_instance.occupation = request.POST['Occupation']

		current_address.street = request.POST['current_street_address']
		current_address.apt = request.POST['apt']
		current_address.city = request.POST['current_address_city']
		current_address.country = request.POST['current_address_country']
		current_address.zip_code = request.POST['current_address_zipcode']

		ph_address.street = request.POST['ph_street_address']
		ph_address.barangay = request.POST['ph_barangay']
		ph_address.city = request.POST['ph_city']
		ph_address.province = request.POST['province']

		if formatDate(request.POST['birth_date']) == False:
			returnVal['error_msg'] = "Date of Birth has format error!"
			return render(request, 'patient_edit.html', returnVal)
		try:
			patient_instance.save()
		except:
			returnVal['error_msg'] = "Error on Saving a Patient"
			return render(request, 'patient_edit.html', returnVal)
		try:
			current_address.save()
		except:
			returnVal['error_msg'] = "Error on Saving Current address!"
			return render(request, 'patient_edit.html', returnVal)
		try:
			ph_address.save()
		except:
			returnVal['error_msg'] = "Error on Saving PH address!"
			return render(request, 'patient_edit.html', returnVal)

		request_file = request.FILES['patientProf'] if 'patientProf' in request.FILES else None
		if request_file:
			split_tup = os.path.splitext(request_file.name)
			file_extension = split_tup[1]
			random_number = random.randint(0,1000)
			fs = FileSystemStorage()
			file_name = "prof_pic/profile_picture_"+str(request.user.id)+"_"+str(random_number)+""+str(file_extension)
			ProfPic = fs.save(file_name, request_file)
			patient_instance.profile_picture = ProfPic
			try:
				patient_instance.save()
			except:
				returnVal['error_msg'] = "Error on Saving a Patient Picture!"
				return render(request, 'patient_edit.html', returnVal)
		return redirect("PatientDetailed", patient_id=patient_instance.pk)
	return render(request, 'patient_edit.html', returnVal)

def formatDate(dateValue):
	current_date_split = dateValue.split("/")
	if len(current_date_split) == 3:
		return current_date_split[2]+"-"+current_date_split[1]+"-"+current_date_split[0]
	else:
		return False





	