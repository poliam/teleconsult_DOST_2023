from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey
from consultation.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime, timedelta


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
	elif request.user.groups.filter(name="Triage").exists():
		returnVal['group_type'] = "Admin"
	returnVal['sidebar'] = "dashboard"
	returnVal['userDetails'] = profile_details
	returnVal['number_of_patients'] = details.objects.filter(status=1).count()
	returnVal['number_of_consultations'] = encounter.objects.filter(status=1).count()

	current_date = date.today()
	future_date = current_date + timedelta(days=7)
	returnVal['week_consultation'] = encounter.objects.filter(consultation_date__range=(current_date, future_date)).order_by('consultation_date')
	returnVal['today_consultation'] = encounter.objects.filter(consultation_date=current_date).order_by('consultation_date')
	returnVal['list_of_patients'] = details.objects.filter(status=1, is_delete=0)
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

def Logout(request):
	logout(request)
	return redirect('login_user')
