from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models import Count, IntegerField
from django.db.models.functions import Cast
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey, details_files
from consultation.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime, timedelta
import os

# Categorizing provinces into Luzon, Visayas, and Mindanao
LUZON_PROVINCES = [
    "ABRA", "ALBAY", "APAYAO", "AURORA", "BATANES", "BATANGAS", "BENGUET", "BULACAN",
    "CAGAYAN", "CAMARINES NORTE", "CAMARINES SUR", "IFUGAO", "ILOCOS NORTE", "ILOCOS SUR",
    "ISABELA", "KALINGA", "LA UNION", "LAGUNA", "MARINDUQUE", "MASBATE", "METRO MANILA",
    "MOUNTAIN PROVINCE", "NUEVA ECIJA", "NUEVA VIZCAYA", "OCCIDENTAL MINDORO", "ORIENTAL MINDORO",
    "PALAWAN", "PAMPANGA", "PANGASINAN", "QUEZON", "QUIRINO", "RIZAL", "ROMBLON", "SORSOGON",
    "TARLAC", "ZAMBALES"
]

VISAYAS_PROVINCES = [
    "AKLAN", "ANTIQUE", "BILIRAN", "BOHOL", "CAPIZ", "CEBU", "EASTERN SAMAR", "GUIMARAS",
    "ILOILO", "LEYTE", "NEGROS OCCIDENTAL", "NEGROS ORIENTAL", "NORTHERN SAMAR",
    "SAMAR", "SOUTHERN LEYTE", "SIQUIJOR", "WESTERN SAMAR"
]

MINDANAO_PROVINCES = [
    "AGUSAN DEL NORTE", "AGUSAN DEL SUR", "BASILAN", "BUKIDNON", "COMPOSTELA VALLEY",
    "COTABATO", "DAVAO DEL NORTE", "DAVAO DEL SUR", "DAVAO OCCIDENTAL", "DAVAO ORIENTAL",
    "DINAGAT ISLANDS", "LANAO DEL NORTE", "LANAO DEL SUR", "MAGUINDANAO", "MISAMIS OCCIDENTAL",
    "MISAMIS ORIENTAL", "NORTH COTABATO", "SARANGANI", "SOUTH COTABATO", "SULTAN KUDARAT",
    "SURIGAO DEL NORTE", "SURIGAO DEL SUR", "ZAMBOANGA DEL NORTE", "ZAMBOANGA DEL SUR",
    "ZAMBOANGA SIBUGAY"
]

@login_required(login_url='/login')
def dashboard(request):
    returnVal = {}
    profile_details = User.objects.get(pk=request.user.id)
    # Determine the group of the logged-in user and set the workplace accordingly
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

    # Default value for workplace_choice if it's not defined above
    if 'workplace_choice' not in locals():
        workplace_choice = None

    # Sidebar and user details
    returnVal['sidebar'] = "dashboard"
    returnVal['userDetails'] = profile_details

    # Filter the number of patients based on workplace choice
    if workplace_choice:
        returnVal['number_of_patients'] = details.objects.filter(status=1, workplace=workplace_choice).count()
        returnVal['number_of_consultations'] = encounter.objects.filter(status=1, details__workplace=workplace_choice).count()
    else:
        returnVal['number_of_patients'] = details.objects.filter(status=1).count()
        returnVal['number_of_consultations'] = encounter.objects.filter(status=1).count()

    # Get upcoming consultations and evaluations within the next week
    current_date = date.today()
    future_date = current_date + timedelta(days=7)

    # Filter 'encounter' objects based on 'consultation_date' within the range and filter by workplace
    if workplace_choice:
        week_consultation = encounter.objects.filter(consultation_date__range=(current_date, future_date), details__workplace=workplace_choice).order_by('consultation_date')
        list_of_psychiatric_evaluate = psychiatric_evaluate.objects.filter(evaluation_consultation_date__range=(current_date, future_date), is_delete=0, details__workplace=workplace_choice).order_by('evaluation_consultation_date')
    else:
        week_consultation = encounter.objects.filter(consultation_date__range=(current_date, future_date)).order_by('consultation_date')
        list_of_psychiatric_evaluate = psychiatric_evaluate.objects.filter(evaluation_consultation_date__range=(current_date, future_date), is_delete=0).order_by('evaluation_consultation_date')

    returnVal['upcomming_appointment'] = week_consultation.count() + list_of_psychiatric_evaluate.count()

    # Filter today's consultations
    if workplace_choice:
        today_consultation = encounter.objects.filter(consultation_date=current_date, is_delete=0, details__workplace=workplace_choice).order_by('consultation_date')
    else:
        today_consultation = encounter.objects.filter(consultation_date=current_date, is_delete=0).order_by('consultation_date')

    today_consultation_list = []
    for consultation in today_consultation:
        try:
            hamd_details = hamd.objects.get(details=consultation.details.pk)
            score = hamd_details.score
        except:
            score = 0
        patient_name = f"{consultation.details.last_name.capitalize()}, {consultation.details.first_name.capitalize()} {consultation.details.middle_name.capitalize()}"
        consulted_by = consultation.consulted_by is not None
        today_consultation_list.append({
            "consultation_id": consultation.pk,
            "consultation_type": consultation.reason_for_interaction,
            "patient_name": patient_name,
            "hamd_score": int(score),
            "consult_by": consulted_by
        })

    returnVal['doctor_today_consultation'] = today_consultation_list
    returnVal['today_consultation'] = today_consultation

    # Filter today's evaluations
    if workplace_choice:
        returnVal['today_evaluation'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date=current_date, is_delete=0, details__workplace=workplace_choice)
    else:
        returnVal['today_evaluation'] = psychiatric_evaluate.objects.filter(evaluation_consultation_date=current_date, is_delete=0)

    # Filter list of patients based on status and workplace
    if workplace_choice:
        returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0, workplace=workplace_choice)
    else:
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
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            errormsg = "Passwords do not match!"
        else:
            # Check if username and email are already in use
            CheckUserByUsername = User.objects.filter(username=request.POST['username'])
            if len(CheckUserByUsername) == 0:
                CheckUserByEmail = User.objects.filter(email=request.POST['email'])
                if len(CheckUserByEmail) == 0:
                    # Create user and assign to group
                    newUser = User.objects.create_user(
                        username=request.POST['username'],
                        email=request.POST['email'],
                        password=password,
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name']
                    )
                    group = Group.objects.get(pk=request.POST['usergroup'])
                    newUser.groups.add(group)
                    success = 1
                    successmsg = "Account created successfully!"
                    return redirect('login_user')  # Redirect to login page
                else:
                    errormsg = "Email is already in use!"
            else:
                errormsg = "Username is already taken!"
    return render(request, "signup.html", {"error_msg": errormsg, "success": success, "successmsg": successmsg})


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

	files = details_files.objects.filter(is_delete=0).order_by('-create_date')
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

	diagnosis_data = (diagnosis.objects.values('condition__name').annotate(count=Count('condition')).order_by('-count'))

	condition_labels = [entry['condition__name'] for entry in diagnosis_data]
	condition_counts = [entry['count'] for entry in diagnosis_data]

	# Score categorization logic
	hamd_data = hamd.objects.annotate(score_int=Cast('score', IntegerField()))
	hamd_conditions = {
		"Normal": hamd_data.filter(score_int__lte=7).count(),
		"Mild Depression": hamd_data.filter(score_int__gt=7, score_int__lt=14).count(),
		"Moderate Depression": hamd_data.filter(score_int__gt=13, score_int__lt=19).count(),
		"Severe Depression": hamd_data.filter(score_int__gt=18, score_int__lt=23).count(),
		"Very Severe Depression": hamd_data.filter(score_int__gte=23).count(),
	}

	# Considering Event Score Categorization
	event_data = considering_event.objects.annotate(score_int=Cast('score_1_16', IntegerField()))

	pgs_conditions = {
		"No Symptoms": event_data.filter(score_int=0).count(),
		"Mild Symptoms": event_data.filter(score_int__lt=11, score_int__gt=0).count(),
		"Moderate-Severe Symptoms": event_data.filter(score_int__gte=11).count(),
	}

	returnVal['pgs_labels'] = list(pgs_conditions.keys())
	returnVal['pgs_counts'] = list(pgs_conditions.values())

	returnVal['hamd_labels'] = list(hamd_conditions.keys())
	returnVal['hamd_counts'] = list(hamd_conditions.values())

	returnVal['condition_labels'] = condition_labels
	returnVal['condition_counts'] = condition_counts

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

	province_data = address.objects.values('ph_province').annotate(count=Count('ph_province'))
	categorized_data = {
		"Luzon": [],
		"Visayas": [],
		"Mindanao": [],
		"Unknown": []
	}
	for item in province_data:
		region = categorize_province(item["ph_province"])
		categorized_data[region].append(item)

	returnVal['occupation_list'] = occupation_list
	returnVal['religion_list'] = religion_list
	returnVal['province_data'] = categorized_data

	return render(request, 'reportTables.html', returnVal)


def categorize_province(province):
	province = province.upper() if province else "UNKNOWN"
	if province in LUZON_PROVINCES:
		return "Luzon"
	elif province in VISAYAS_PROVINCES:
		return "Visayas"
	elif province in MINDANAO_PROVINCES:
		return "Mindanao"
	return "Unknown"