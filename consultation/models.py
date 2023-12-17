from django.db import models
from django.contrib.auth.models import User
from patient.models import details, medicine

# Create your models here.

class dress_and_grooming(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class attitude(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class facialexpression(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class motoactive(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class movement(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class speech(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class aphasia(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class mood(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class affect(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class insomnia(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class orientation(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class memory(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class disorderedperception(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class thoughtcontent(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class delusioncontent(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class thoughtform(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class preoccupation(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	def __str__(self):
		return self.name

class condition(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class encounter(models.Model):
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	reason_for_interaction = models.CharField(max_length=250, null=True, blank=True)
	encounter_notes = models.TextField(null=True, blank=True)
	treatment_recommendations = models.TextField(null=True, blank=True)
	consultation_date = models.DateField(null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='update_by')
	consulted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
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

class history_present_illness(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	number = models.CharField(max_length=250, null=True, blank=True)
	calendrical = models.CharField(max_length=250, null=True, blank=True)
	details = models.TextField(null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class mental_general_description(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)

	dress_grooming = models.ForeignKey(dress_and_grooming, null=True, blank=True, on_delete=models.SET_NULL)
	physical_characteristics = models.TextField(null=True, blank=True)
	posture_gait = models.TextField(null=True, blank=True)

	attitude = models.ForeignKey(attitude, null=True, blank=True, on_delete=models.SET_NULL)
	facial_expression = models.ForeignKey(facialexpression, null=True, blank=True, on_delete=models.SET_NULL)
	motor_active = models.ForeignKey(motoactive, null=True, blank=True, on_delete=models.SET_NULL)
	movement = models.ForeignKey(movement, null=True, blank=True, on_delete=models.SET_NULL)

	behavior_remarks = models.TextField(null=True, blank=True)

	speech = models.ForeignKey(speech, null=True, blank=True, on_delete=models.SET_NULL)
	aphasia = models.ForeignKey(aphasia, null=True, blank=True, on_delete=models.SET_NULL)
	remarks = models.TextField(null=True, blank=True)

	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class mental_emotions(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)

	mood = models.ForeignKey(mood, null=True, blank=True, on_delete=models.SET_NULL)
	affect = models.ForeignKey(affect, null=True, blank=True, on_delete=models.SET_NULL)
	sign_depression = models.ForeignKey(insomnia, null=True, blank=True, on_delete=models.SET_NULL)
	emotion_remarks = models.TextField(null=True, blank=True)

	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class mental_cognitive_function(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	consciousness = models.ForeignKey(orientation, null=True, blank=True, on_delete=models.SET_NULL)
	memory = models.ForeignKey(memory, null=True, blank=True, on_delete=models.SET_NULL)
	attention = models.BooleanField(default=0)
	concentrate = models.BooleanField(default=0)
	memory_remarks = models.TextField(null=True, blank=True)
	abstractability_remarks = models.TextField(null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class mental_thought_perception(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	disordered_perception = models.ForeignKey(disorderedperception, null=True, blank=True, on_delete=models.SET_NULL)
	thought_content = models.ForeignKey(thoughtcontent, null=True, blank=True, on_delete=models.SET_NULL)
	delusion_content = models.ForeignKey(delusioncontent, null=True, blank=True, on_delete=models.SET_NULL)
	thought_form = models.ForeignKey(thoughtform, null=True, blank=True, on_delete=models.SET_NULL)
	preoccupations = models.ForeignKey(preoccupation, null=True, blank=True, on_delete=models.SET_NULL)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class suicidality(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	is_suicidal = models.BooleanField(default=0)
	suicidality_remarks = models.TextField(null=True, blank=True)
	is_homicidal = models.BooleanField(default=0)
	impulse_remarks = models.TextField(null=True, blank=True)

	reliability = models.TextField(null=True, blank=True)
	reliability_impression = models.TextField(null=True, blank=True)

	surroundings_inappropriate = models.BooleanField(default=0)
	environment = models.TextField(null=True, blank=True)
	environment_remarks = models.TextField(null=True, blank=True)

	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class diagnosis(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	condition = models.ForeignKey(condition, null=True, blank=True, on_delete=models.SET_NULL)
	condition_details = models.TextField(null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class treatment(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	drugs = models.ForeignKey(medicine, null=True, blank=True, on_delete=models.SET_NULL)
	strength = models.CharField(max_length=250, null=True, blank=True)
	dose = models.CharField(max_length=250, null=True, blank=True)
	route = models.CharField(max_length=250, null=True, blank=True)
	frequency = models.CharField(max_length=250, null=True, blank=True)
	drug_no = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)


class Referral(models.Model):
	encounter = models.ForeignKey(encounter, null=True, blank=True, on_delete=models.SET_NULL)
	referred_to = models.CharField(max_length=250, null=True, blank=True)
	referred_from = models.CharField(max_length=250, null=True, blank=True)
	brief_summary = models.TextField(null=True, blank=True)
	impression = models.TextField(null=True, blank=True)
	reason_for_referral = models.TextField(null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	create_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)
	