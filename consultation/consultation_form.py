from django import forms
from patient.models import details
from consultation.models import *

REASON_FOR_INTERACTION = (
    ("Outpatient", "Outpatient - Checkup"),
    ("Followup", "Outpatient - Followup")
)

RELATIONSHIP_CHOICES = (
	(0, "- - Select Relationship - -"),
	("Mother", "Mother"),
	("Father", "Father"),
	("Son", "Son"),
	("Daughter", "Daughter"),
	("Brother", "Brother"),
	("Niece or nephew", "Niece or nephew"),
	("Aunt", "Aunt"),
	("Uncle", "Uncle"),
	("Sister", "Sister"),
	("Spouse", "Spouse"),
	("Son-in-law", "Son-in-law"),
	("Daughter-in-law", "Daughter-in-law"),
	("Second Cousin", "Second Cousin"),
	("Third Cousin", "Third Cousin"),
	("Wife", "Wife"),
	("Husband", "Husband"),
	("Friend", "Friend"),
	("Guardian", "Guardian"),
)

class AddConsultationEncounterForm(forms.ModelForm):
	reason_for_interaction = forms.TypedChoiceField(required=True, label="Reason For Interaction", choices=REASON_FOR_INTERACTION)
	consultation_date = forms.DateField(required=True, label="Consultation(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	encounter_notes = forms.CharField(required=False, label="Notes", widget=forms.Textarea(attrs={'rows':4}))
	treatment_recommendations = forms.CharField(required=False, label="Treatment Recommendations", widget=forms.Textarea(attrs={'rows':4}))

	def __init__(self, *args, **kwargs):
		super(AddConsultationEncounterForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = encounter
		fields = ['reason_for_interaction', 'consultation_date', 'encounter_notes', 'treatment_recommendations']

class AddConsultationVitalSignForm(forms.ModelForm):
	height = forms.CharField(required=False, label="Height(cm)", widget=forms.TextInput(attrs={'placeholder': 'Height'}))
	weight = forms.CharField(required=False, label="Weight(kg)", widget=forms.TextInput(attrs={'placeholder': 'Weight'}))
	blood_pressure = forms.CharField(required=False, label="Blood Pressure", widget=forms.TextInput(attrs={'placeholder': 'Blood Pressure'}))
	temperature = forms.CharField(required=False, label="Temperature(c)", widget=forms.TextInput(attrs={'placeholder': 'Temperature'}))

	def __init__(self, *args, **kwargs):
		super(AddConsultationVitalSignForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = vitalsign
		fields = ['height', 'weight', 'blood_pressure', 'temperature']

class AddConsultationChiefComplaintForm(forms.ModelForm):
	patient_complaints = forms.CharField(required=False, label="Patient Complaints", widget=forms.Textarea(attrs={'rows':4}))
	informant_complaints = forms.CharField(required=False, label="Informant Complaints", widget=forms.Textarea(attrs={'rows':4}))
	informatmant_relationship = forms.TypedChoiceField(required=True, label="Informant Relationshop", choices=RELATIONSHIP_CHOICES)

	def __init__(self, *args, **kwargs):
		super(AddConsultationChiefComplaintForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = chief_complaints
		fields = ['patient_complaints', 'informant_complaints', 'informatmant_relationship']

class AddMentalGeneralDescriptionForm(forms.ModelForm):
	dress_grooming = forms.ModelChoiceField(required=False, label="Dress Grooming", queryset=dress_and_grooming.objects.all().order_by("name"))
	physical_characteristics = forms.CharField(required=False, label="Physical Characteristics", widget=forms.Textarea(attrs={'rows':3}))
	posture_gait = forms.CharField(required=False, label="Posture Gait", widget=forms.Textarea(attrs={'rows':3}))
	attitude = forms.ModelChoiceField(required=False, label="Attitude", queryset=attitude.objects.all().order_by("name"))
	facial_expression = forms.ModelChoiceField(required=False, label="Facial Expression", queryset=facialexpression.objects.all().order_by("name"))
	motor_active = forms.ModelChoiceField(required=False, label="Motor Active", queryset=motoactive.objects.all().order_by("name"))
	movement = forms.ModelChoiceField(required=False, label="Movement", queryset=movement.objects.all().order_by("name"))
	behavior_remarks = forms.CharField(required=False, label="Behavior Remarks", widget=forms.Textarea(attrs={'rows':3}))
	speech = forms.ModelChoiceField(required=False, label="Speech", queryset=speech.objects.all().order_by("name"))
	aphasia = forms.ModelChoiceField(required=False, label="Aphasia", queryset=aphasia.objects.all().order_by("name"))
	remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(attrs={'rows':3}))

	def __init__(self, *args, **kwargs):
		super(AddMentalGeneralDescriptionForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = mental_general_description
		fields = ['dress_grooming', 'physical_characteristics', 'posture_gait', 'attitude', 'facial_expression', 'motor_active', 'movement', 'behavior_remarks', 'speech', 'aphasia', 'remarks']

class AddMentalEmotionForm(forms.ModelForm):
	mood = forms.ModelChoiceField(required=False, label="Mood", queryset=mood.objects.all().order_by("name"))
	affect = forms.ModelChoiceField(required=False, label="Affect", queryset=affect.objects.all().order_by("name"))
	sign_depression = forms.ModelChoiceField(required=False, label="Sign of Depression", queryset=insomnia.objects.all().order_by("name"))
	emotion_remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(attrs={'rows':3}))

	def __init__(self, *args, **kwargs):
		super(AddMentalEmotionForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = mental_emotions
		fields = ['mood', 'affect', 'sign_depression', 'emotion_remarks']

class AddMentalCognitiveForm(forms.ModelForm):
	consciousness = forms.ModelChoiceField(required=False, label="Consciousness", queryset=orientation.objects.all().order_by("name"))
	memory = forms.ModelChoiceField(required=False, label="Memory", queryset=memory.objects.all().order_by("name"))
	attention = forms.BooleanField(label='Is able to pay attention', required=False)
	concentrate = forms.BooleanField(label='Is able to concentrate', required=False)
	memory_remarks = forms.CharField(required=False, label="Memory Remarks", widget=forms.Textarea(attrs={'rows':3}))
	abstractability_remarks = forms.CharField(required=False, label="Abstractability Remarks", widget=forms.Textarea(attrs={'rows':3}))

	def __init__(self, *args, **kwargs):
		super(AddMentalCognitiveForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'
		self.fields["attention"].widget.attrs.update({"class": "form-check-input"})
		self.fields["concentrate"].widget.attrs.update({"class": "form-check-input"})

	class Meta:
		model = mental_cognitive_function
		fields = ['consciousness', 'memory', 'attention', 'concentrate', 'memory_remarks', 'abstractability_remarks']

class AddMentalThoughtPerceptionForm(forms.ModelForm):
	disordered_perception = forms.ModelChoiceField(required=False, label="Disordered Perceptions", queryset=disorderedperception.objects.all().order_by("name"))
	thought_content = forms.ModelChoiceField(required=False, label="Thought Content", queryset=thoughtcontent.objects.all().order_by("name"))
	delusion_content = forms.ModelChoiceField(required=False, label="Delusion Content", queryset=delusioncontent.objects.all().order_by("name"))
	thought_form = forms.ModelChoiceField(required=False, label="Thought Form", queryset=thoughtform.objects.all().order_by("name"))
	preoccupations = forms.ModelChoiceField(required=False, label="Preoccupations", queryset=preoccupation.objects.all().order_by("name"))

	def __init__(self, *args, **kwargs):
		super(AddMentalThoughtPerceptionForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = mental_thought_perception
		fields = ['disordered_perception', 'thought_content', 'delusion_content', 'thought_form', 'preoccupations']

class AddMentalSuicidalityForm(forms.ModelForm):
	is_suicidal = forms.BooleanField(label='Is patient suicidal?', required=False)
	suicidality_remarks = forms.CharField(required=False, label="Suicidality homicidality Remarks", widget=forms.Textarea(attrs={'rows':3}))
	is_homicidal = forms.BooleanField(label='Is patient homicidal?', required=False)
	impulse_remarks = forms.CharField(required=False, label="Impulse Remarks", widget=forms.Textarea(attrs={'rows':3}))

	reliability = forms.CharField(required=False, label="Reliability", widget=forms.Textarea(attrs={'rows':3}))
	reliability_impression = forms.CharField(required=False, label="Reliability Impression", widget=forms.Textarea(attrs={'rows':3}))

	surroundings_inappropriate = forms.BooleanField(label='Is surroundings inappropriate?', required=False)
	environment = forms.CharField(required=False, label="Environment", widget=forms.Textarea(attrs={'rows':3}))
	environment_remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(attrs={'rows':3}))


	def __init__(self, *args, **kwargs):
		super(AddMentalSuicidalityForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'
		self.fields["is_suicidal"].widget.attrs.update({"class": "form-check-input"})
		self.fields["is_homicidal"].widget.attrs.update({"class": "form-check-input"})
		self.fields["surroundings_inappropriate"].widget.attrs.update({"class": "form-check-input"})

	class Meta:
		model = suicidality
		fields = ['is_suicidal', 'is_homicidal', 'suicidality_remarks', 'impulse_remarks', 'reliability', 'reliability_impression', 'surroundings_inappropriate', 'environment', 'environment_remarks']

class AddReferralForm(forms.ModelForm):
	referred_to = forms.CharField(required=False, label="Referred To", widget=forms.TextInput(attrs={'placeholder': 'Referred To'}))
	referred_from = forms.CharField(required=False, label="Referred From", widget=forms.TextInput(attrs={'placeholder': 'Referred From'}))
	brief_summary = forms.CharField(required=False, label="Brief Summary", widget=forms.Textarea(attrs={'rows':3}))
	impression = forms.CharField(required=False, label="Impression", widget=forms.Textarea(attrs={'rows':3}))
	reason_for_referral = forms.CharField(required=False, label="Reason For Referral", widget=forms.Textarea(attrs={'rows':3}))


	def __init__(self, *args, **kwargs):
		super(AddReferralForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'


	class Meta:
		model = Referral
		fields = ['referred_to', 'referred_from', 'brief_summary', 'impression', 'reason_for_referral']

