from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class details(models.Model):
	first_name = models.CharField(max_length=250, null=True, blank=True)
	middle_name = models.CharField(max_length=250, null=True, blank=True)
	last_name = models.CharField(max_length=250, null=True, blank=True)
	gender = models.CharField(max_length=250, null=True, blank=True)
	gender_indentity = models.CharField(max_length=250, null=True, blank=True)
	BOD = models.DateField(null=True, blank=True)
	marital_status = models.CharField(max_length=250, null=True, blank=True)
	contact_number = models.CharField(max_length=250, null=True, blank=True)
	alias = models.CharField(max_length=250, null=True, blank=True)
	email = models.CharField(max_length=250, null=True, blank=True)
	birth_place = models.CharField(max_length=250, null=True, blank=True)
	religion = models.CharField(max_length=250, null=True, blank=True)
	high_education = models.CharField(max_length=250, null=True, blank=True)
	citizenship = models.CharField(max_length=250, null=True, blank=True)
	nationality = models.CharField(max_length=250, null=True, blank=True)
	workplace = models.CharField(max_length=250, null=True, blank=True)
	occupation = models.CharField(max_length=250, null=True, blank=True)
	profile_picture = models.FileField(upload_to='prof_pic/', null=True, blank=True)
	employment_status = models.CharField(max_length=250, null=True, blank=True)
	mental_health_history = models.CharField(max_length=250, null=True, blank=True)
	access_to_mental_health = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	@property
	def age(self):
		return int((datetime.now().date() - self.BOD).days / 365.25)

class address(models.Model):
	current_street = models.CharField(max_length=250, null=True, blank=True, default="")
	current_apt = models.CharField(max_length=250, null=True, blank=True, default="")
	current_barangay = models.CharField(max_length=250, null=True, blank=True, default="")
	current_province = models.CharField(max_length=250, null=True, blank=True, default="")
	current_city = models.CharField(max_length=250, null=True, blank=True, default="")
	current_country = models.CharField(max_length=250, null=True, blank=True, default="")
	current_zip_code = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_street = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_apt = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_barangay = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_province = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_city = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_country = models.CharField(max_length=250, null=True, blank=True, default="")
	ph_zip_code = models.CharField(max_length=250, null=True, blank=True, default="")
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	
class relatives(models.Model):
	first_name = models.CharField(max_length=250, null=True, blank=True)
	middle_name = models.CharField(max_length=250, null=True, blank=True)
	last_name = models.CharField(max_length=250, null=True, blank=True)
	gender = models.CharField(max_length=250, null=True, blank=True)
	gender_indentity = models.CharField(max_length=250, null=True, blank=True)
	DOB = models.DateField(null=True, blank=True)
	marital_status = models.CharField(max_length=250, null=True, blank=True)
	relationship = models.CharField(max_length=250, null=True, blank=True)
	high_education = models.CharField(max_length=250, null=True, blank=True)
	occupation = models.CharField(max_length=250, null=True, blank=True)
	Workplace = models.CharField(max_length=250, null=True, blank=True)
	contact_number = models.CharField(max_length=250, null=True, blank=True)
	email = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	is_emergency = models.BooleanField(default=0)

	@property
	def age(self):
		return int((datetime.now().date() - self.DOB).days / 365.25)

class medicine(models.Model):
	name = models.CharField(max_length=250, null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class allergies(models.Model):
	medicine_name = models.ForeignKey(medicine, null=True, blank=True, on_delete=models.SET_NULL)
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	is_delete = models.BooleanField(default=0)

class global_psychotrauma_screen(models.Model):
	EVENT_CHOICES = [
		('last week', 'last week'),
		('last month', 'last month'),
		('last half year', 'last half year'),
		('last year', 'last year'),
		('longer ago', 'longer ago'),
	]
	
	VIOLENCE_CHOICES = [
		('to yourself', 'to yourself'),
		('happened to someone else', 'happened to someone else'),
	]
	
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	consultation_date = models.DateTimeField(auto_now_add=True)
	event_description = models.TextField(null=True, blank=True)
	event_happened = models.CharField(max_length=20, choices=EVENT_CHOICES, null=True, blank=True)
	physical_violence = models.CharField(max_length=30, choices=VIOLENCE_CHOICES, default='to yourself', null=False, blank=False)
	sexual_violence = models.CharField(max_length=30, choices=VIOLENCE_CHOICES, default='to yourself', null=False, blank=False)
	emotional_abuse = models.CharField(max_length=30, choices=VIOLENCE_CHOICES, default='to yourself', null=False, blank=False)
	serious_injury = models.CharField(max_length=30, choices=VIOLENCE_CHOICES, default='to yourself', null=False, blank=False)
	life_threatening = models.CharField(max_length=30, choices=VIOLENCE_CHOICES, default='to yourself', null=False, blank=False)
	sudden_death_of_loved_one = models.BooleanField(default=0)
	cause_harm_to_others = models.BooleanField(default=0)
	covid = models.BooleanField(default=0)
	single_event_occurring = models.CharField(max_length=250, null=True, blank=True)
	range_event_occurring_from = models.CharField(max_length=250, null=True, blank=True)
	range_event_occurring_to = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)
	
	class Meta:
		constraints = [
			models.CheckConstraint(
				check=~models.Q(details=None),
				name='gps_details_required'
			)
		]
	
	def clean(self):
		if not self.details:
			raise ValidationError('Details is required.')
		if self.event_happened and self.event_happened not in dict(self.EVENT_CHOICES):
			raise ValidationError('Invalid event_happened choice.')
	
	def save(self, *args, **kwargs):
		self.full_clean()
		# Always include update_date in update_fields if specified
		if 'update_fields' in kwargs and 'update_date' not in kwargs['update_fields']:
			kwargs['update_fields'] = list(kwargs['update_fields']) + ['update_date']
		super().save(*args, **kwargs)

class considering_event(models.Model):
	YES_NO_CHOICES = [
		('No', 'No'),
		('Yes', 'Yes'),
	]
	
	RATING_CHOICES = [
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
	]
	
	global_psychotrauma_screen = models.ForeignKey(global_psychotrauma_screen, null=True, blank=True, on_delete=models.CASCADE)
	considering_event_1 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_2 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_3 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_4 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_5 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_6 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_7 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_8 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_9 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_10 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_11 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_12 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_13 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_14 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_15 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_16 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_17 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_18 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_19 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_20 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_21 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_22 = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', null=False, blank=False)
	considering_event_23 = models.CharField(max_length=3, choices=RATING_CHOICES, default='1', null=False, blank=False)
	score_1_16 = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
	total_score = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

	
	def clean(self):
		# Count "Yes" events
		events = [getattr(self, f'considering_event_{i}') for i in range(1, 24)]
		yes_events = [e for e in events if e == 'Yes']
		
		if not yes_events:
			raise ValidationError('At least one considering event must be set to Yes.')
		
		# Check maximum limit per GPS
		if self.global_psychotrauma_screen_id:
			total_events = considering_event.objects.filter(
				global_psychotrauma_screen=self.global_psychotrauma_screen
			).exclude(pk=self.pk).count()
			
			if total_events >= 15:
				raise ValidationError('Maximum of 15 considering events per screen allowed.')
	
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

class hamd(models.Model):
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	consultation_date = models.DateTimeField(auto_now_add=True)
	score = models.CharField(max_length=250, blank=True, null=True)
	total_score = models.CharField(max_length=250, blank=True, null=True)
	depressed_mood = models.CharField(max_length=250, null=True, blank=True)
	feeling_of_guilt = models.CharField(max_length=250, null=True, blank=True)
	suicide = models.CharField(max_length=250, null=True, blank=True)
	insomnia_initial = models.CharField(max_length=250, null=True, blank=True)
	insomnia_middle = models.CharField(max_length=250, null=True, blank=True)
	insomnia_delayed = models.CharField(max_length=250, null=True, blank=True)
	work_and_interests = models.CharField(max_length=250, null=True, blank=True)
	retardation_delayed = models.CharField(max_length=250, null=True, blank=True)
	agitation_delayed = models.CharField(max_length=250, null=True, blank=True)
	anxiety_psychic = models.CharField(max_length=250, null=True, blank=True)
	anxiety_somatic = models.CharField(max_length=250, null=True, blank=True)
	somatic_symptoms_gastrointestinal = models.CharField(max_length=250, null=True, blank=True)
	somatic_symptoms_general = models.CharField(max_length=250, null=True, blank=True)
	genital_symptoms = models.CharField(max_length=250, null=True, blank=True)
	hypochondriasis = models.CharField(max_length=250, null=True, blank=True)
	weight_loss = models.CharField(max_length=250, null=True, blank=True)
	insight = models.CharField(max_length=250, null=True, blank=True)
	diurnal_variation = models.CharField(max_length=250, null=True, blank=True)
	diurnal_variation_mild_am = models.BooleanField(default=0)
	diurnal_variation_mild_pm = models.BooleanField(default=0)
	diurnal_variation_severe_am = models.BooleanField(default=0)
	diurnal_variation_severe_pm = models.BooleanField(default=0)
	depersonalization_and_derelization = models.CharField(max_length=250, null=True, blank=True)
	paranoid_symptoms = models.CharField(max_length=250, null=True, blank=True)
	obsessional_symptoms = models.CharField(max_length=250, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class patient_survey(models.Model):
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	responde_date = models.DateTimeField(auto_now_add=True)
	
	social_phobia = models.CharField(max_length=250, blank=True, null=True)
	generalized_anxiety_disorder = models.CharField(max_length=250, blank=True, null=True)
	major_depressive_disorder = models.CharField(max_length=250, blank=True, null=True)
	disorder_personality_disorder = models.CharField(max_length=250, blank=True, null=True)
	dysthymia = models.CharField(max_length=250, blank=True, null=True)
	agoraphobia = models.CharField(max_length=250, blank=True, null=True)
	bipolar_disorder = models.CharField(max_length=250, blank=True, null=True)
	drug_dependence = models.CharField(max_length=250, blank=True, null=True)
	mas_babae = models.CharField(max_length=250, blank=True, null=True)
	mas_lalake = models.CharField(max_length=250, blank=True, null=True)

	kalidad_pagtulog = models.CharField(max_length=250, blank=True, null=True)
	iwasan_aktibidad = models.CharField(max_length=250, blank=True, null=True)

	cognitive_behavior_therapy = models.CharField(max_length=250, blank=True, null=True)
	kumpidensyal = models.CharField(max_length=250, blank=True, null=True)
	hindi_nagbabanta = models.CharField(max_length=250, blank=True, null=True)

	hahanapin_impormasyon_sakit_isip = models.CharField(max_length=250, blank=True, null=True)
	humingi_impormasyon_sakit_isip = models.CharField(max_length=250, blank=True, null=True)
	pagpapatingin_sa_doktor = models.CharField(max_length=250, blank=True, null=True)
	mapagkukunan_impormasyon_sakit_isip = models.CharField(max_length=250, blank=True, null=True)
	bumalik_tamang_kaisipan = models.CharField(max_length=250, blank=True, null=True)
	personal_kahinaan = models.CharField(max_length=250, blank=True, null=True)
	sakit_medikal = models.CharField(max_length=250, blank=True, null=True)
	mapanganib = models.CharField(max_length=250, blank=True, null=True)
	umiwas_taong_sakit_isip = models.CharField(max_length=250, blank=True, null=True)
	hindi_sasabihin_kahit_kanino = models.CharField(max_length=250, blank=True, null=True)
	question_26 = models.CharField(max_length=250, blank=True, null=True)
	question_27 = models.CharField(max_length=250, blank=True, null=True)
	hindi_magiging_epektibo = models.CharField(max_length=250, blank=True, null=True)

	lumipat_ng_bahay = models.CharField(max_length=250, blank=True, null=True)
	pakikisalamuha_isang_taong = models.CharField(max_length=250, blank=True, null=True)
	question_31 = models.CharField(max_length=250, blank=True, null=True)
	question_32 = models.CharField(max_length=250, blank=True, null=True)
	question_33 = models.CharField(max_length=250, blank=True, null=True)
	question_34 = models.CharField(max_length=250, blank=True, null=True)
	question_35 = models.CharField(max_length=250, blank=True, null=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class details_files(models.Model):
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	file_name = models.CharField(max_length=250, null=True, blank=True)
	file = models.FileField(upload_to='files/', null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)


class details_audit(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_edited')
	url = models.CharField(max_length=250, blank=True, null=True)
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL)
	create_date = models.DateTimeField(auto_now_add=True)
	updated_fields = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)






















