from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models import Count
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey, details_files
from consultation.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime, timedelta
import os



@login_required(login_url='/login')
def dashboard(request):
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
	returnVal['sidebar'] = "dashboard"
	returnVal['userDetails'] = profile_details
	returnVal['number_of_patients'] = details.objects.filter(status=1).count()
	returnVal['number_of_consultations'] = encounter.objects.filter(status=1).count()

	current_date = date.today()
	future_date = current_date + timedelta(days=7)
	week_consultation = encounter.objects.filter(consultation_date__range=(current_date, future_date)).order_by('consultation_date')
	list_of_psychiatric_evaluate = psychiatric_evaluate.objects.filter(evaluation_consultation_date__range=(current_date, future_date), is_delete=0).order_by('evaluation_consultation_date')
	returnVal['upcomming_appointment'] = week_consultation.count() + list_of_psychiatric_evaluate.count()
	today_consultation = encounter.objects.filter(consultation_date=current_date, is_delete=0).order_by('consultation_date')
	today_consultation_list = []
	for consultation in today_consultation:
		try:
			hamd_details = hamd.objects.get(details=consultation.details.pk)
			score = hamd_details.score
		except:
			score = 0
		patient_name = consultation.details.last_name.capitalize()+", "+consultation.details.first_name.capitalize()+" "+consultation.details.middle_name.capitalize()
		if consultation.consulted_by is None:
			consulted_by = False
		else:
			consulted_by = True
		today_consultation_list.append({"consultation_id": consultation.pk, "consultation_type": consultation.reason_for_interaction, "patient_name": patient_name, "hamd_score": int(score), "consult_by": consulted_by})
	returnVal['doctor_today_consultation'] = today_consultation_list
	returnVal['today_consultation'] = today_consultation


	returnVal['today_evaluation'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date=current_date, is_delete=0)
	returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0)
	current_date_split = str(current_date).split("-")
	return render(request, 'dashboard.html', returnVal)

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.GET.get('next') != None:
				return redirect(request.GET.get('next'),  '/')
			return redirect('dashboard')
		else:
			return render(request, 'login.html' , {"error_msg": "username and password does not match!", "username":username})
	else:
		return render(request, 'login.html', {"error_msg": "", "username": ""})

def signup(request):
	errormsg = ""
	successmsg = ""
	success = 0
	if request.method == 'POST':
		CheckUserByUsername = User.objects.filter(username=request.POST['username'])
		if len(CheckUserByUsername) == 0:
			CheckUserByEmail = User.objects.filter(email=request.POST['email'])
			if len(CheckUserByEmail) == 0:
				newUser = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
				group = Group.objects.get(pk=request.POST['usergroup'])
				newUser.groups.add(group)
				success = 1
				successmsg = "Create Account Success!"
			else:
				errormsg = "Email already been used!"
		else:
			errormsg = "Username Already Taken!"
	return render(request, "signup.html", {"error_msg":errormsg, "success": success, "successmsg": successmsg})

def change_password(request):
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
	returnVal['sidebar'] = "settings"
	returnVal['userDetails'] = profile_details

	if request.method == 'POST':
		username = request.POST.get('username')
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return render(request, 'errorPage.html', {'error_message': 'User does not exist.'})
		if not user.check_password(old_password):
			return render(request, 'errorPage.html', {'error_message': 'Old password is incorrect.'})

		# Set new password
		user.set_password(new_password)
		user.save()

		# Logout the user
		logout(request)

		return redirect('login_user')
	else:
		return render(request, 'changePassword.html', returnVal)

def Logout(request):
	logout(request)
	return redirect('login_user')

def reportPage(request):
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
	returnVal['sidebar'] = "reports"
	returnVal['userDetails'] = profile_details

	files = details_files.objects.filter(is_delete=0)
	returnVal['list_of_files'] = files
	

	return render(request, 'report_page.html', returnVal)

def download_file(request, file_id):
	filesDetails = get_object_or_404(details_files, id=file_id)
	file_field = filesDetails.file  # This is a FieldFile object

	# Use .path to get the file path
	file_path = file_field.path

	# Now you can use os.stat or other functions that require a file path
	file_stat = os.stat(file_path)
	# file_path = os.path.join(settings.MEDIA_ROOT, filename)
	if os.path.exists(file_path):
		response = FileResponse(open(file_path, 'rb'))
		return response
	else:
		raise Http404("File does not exist")



def reportCharts(request):
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
	returnVal['sidebar'] = "reports"
	returnVal['userDetails'] = profile_details

	# Get year and month from query parameters with defaults
	selected_year = request.GET.get('year', datetime.now().year)
	selected_month = request.GET.get('month', '')

	# Build query filter dynamically
	filters = {}
	if selected_year:
		filters['create_date__year'] = selected_year
	if selected_month:
		filters['create_date__month'] = selected_month

	# Query the filtered data
	gender_data = details.objects.filter(**filters).values('gender').annotate(count=Count('gender'))

	# Prepare data for the chart
	gender_counts = {entry['gender']: entry['count'] for entry in gender_data}
	male_count = gender_counts.get('Male', 0)
	female_count = gender_counts.get('Female', 0)

	# Educational Attainment Report Data
	education_data = details.objects.values('high_education').annotate(count=Count('high_education'))
	education_labels = [entry['high_education'] for entry in education_data]
	education_counts = [entry['count'] for entry in education_data]

	# Marital Status Report Data
	marital_data = details.objects.values('marital_status').annotate(count=Count('marital_status'))
	marital_counts = {entry['marital_status']: entry['count'] for entry in marital_data}
	single_count = marital_counts.get('Single', 0)
	married_count = marital_counts.get('Married', 0)
	widowed_count = marital_counts.get('Widowed', 0)
	divorced_count = marital_counts.get('Divorced', 0)
	separated_count = marital_counts.get('Separated', 0)
	cohabiting_count = marital_counts.get('Cohabiting', 0)

	# Get distinct years from the database for the year dropdown
	available_years = details.objects.dates('create_date', 'year').distinct().values_list('create_date__year', flat=True)



	returnVal['male_count'] = male_count
	returnVal['female_count'] = female_count
	returnVal['selected_month'] = selected_month
	returnVal['selected_year'] = int(selected_year)
	returnVal['available_years'] = available_years

	returnVal['single_count'] = single_count
	returnVal['married_count'] = married_count
	returnVal['widowed_count'] = widowed_count
	returnVal['divorced_count'] = divorced_count
	returnVal['separated_count'] = separated_count
	returnVal['cohabiting_count'] = cohabiting_count

	returnVal['education_labels'] = education_labels
	returnVal['education_counts'] = education_counts

	return render(request, 'genderReportSections.html', returnVal)

def reportTables(request):
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
	returnVal['sidebar'] = "reports"
	returnVal['userDetails'] = profile_details

	# Retrieve occupation counts
	occupation_data = details.objects.values('occupation').annotate(count=Count('occupation'))
	total_count = sum(entry['count'] for entry in occupation_data)

	# Prepare data for template
	occupation_list = []
	for entry in occupation_data:
		percentage = (entry['count'] / total_count) * 100 if total_count > 0 else 0
		occupation_list.append({
			'occupation': entry['occupation'] or 'Unknown',
			'count': entry['count'],
			'percentage': f'{percentage:.2f}%'
		})

	# Fetch religion data
	religion_data = details.objects.values('religion').annotate(count=Count('religion'))
	total_religion = sum(entry['count'] for entry in religion_data)
	religion_list = [
		{
			'religion': entry['religion'] or 'Unknown',
			'count': entry['count'],
			'percentage': f"{(entry['count'] / total_religion * 100):.2f}%" if total_religion > 0 else "0%"
		}
		for entry in religion_data
	]


	returnVal['occupation_list'] = occupation_list
	returnVal['religion_list'] = religion_list

	return render(request, 'reportTables.html', returnVal)
