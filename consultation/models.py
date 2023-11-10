from django.db import models
from patient.models import details

# Create your models here.

class dress_and_grooming(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class attitude(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class facialexpression(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class motoactive(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class movement(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class speech(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class aphasia(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class mood(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class affect(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class insomnia(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class orientation(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class memory(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class disorderedperception(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class thoughtcontent(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class delusioncontent(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class thoughtform(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class preoccupation(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class condition(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class encounter(models.Model):
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	reason_for_interaction = models.CharField(max_length=250, null=True, blank=True)
	cconsultation_date = models.DateTimeField(auto_now_add=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class vitalsign(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	height = models.CharField(max_length=250, null=True, blank=True)
	weight = models.CharField(max_length=250, null=True, blank=True)
	blood_pressure = models.CharField(max_length=250, null=True, blank=True)
	temperature = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class chief_complaints(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	patient_complaints = models.TextField(null=True, blank=True)
	informant_complaints = models.TextField(null=True, blank=True)
	informatmant_relationship = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	