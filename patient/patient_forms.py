from django import forms
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd, patient_survey, details_files
from django.core.validators import validate_email
from datetime import date
from .models import details

SEX_CHOICES = (
	("", "- - Select Sex - -"),
    ("Male", "Male"),
    ("Female", "Female")
)

YES_NO_CHOICES = [
	(0, "No"), 
	(1, "Yes")
]

YES_NO_TEXT_CHOICES = [
	("No", "No"), 
	("Yes", "Yes")
]

WORKPLACE_CHOICES = [
	("Riyadh", "Riyadh"), 
	("Jeddah", "Jeddah")
]

EMPLOYMENT_STATUS_CHOICES = [
	("Currently Employed", "Currently Employed"), 
	("Previously Employed", "Previously Employed"),
	("Unemployed", "Unemployed")
]

MARITAL_CHOICES = (
	("0", "- - Select Status - -"),
	("Single", "Single"),
	("Married", "Married"),
	("Widowed", "Widowed"),
	("Divorced", "Divorced"),
	("Separated", "Separated"),
	("Cohabiting", "Cohabiting")
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

SECTION_I_CHOICES = (
	("Lubos na Maari", "Lubos na Maari"), 
	("Maaari", "Maaari"),
	("Hindi Maaari", "Hindi Maaari"),
	("Lubos na Hindi Maaari", "Lubos na Hindi Maaari"),
)

SECTION_II_CHOICES = (
	("Labis na Nakakatulong", "Labis na Nakakatulong"),
	("Nakakatulong", "Nakakatulong"),
	("Hindi Nakakatulong", "Hindi Nakakatulong"),
	("Labis na Hindi Nakakatulong", "Labis na Hindi Nakakatulong"),
)

SECTION_IV_CHOICES = (
	("Strongly Agree", "Strongly Agree"),
	("Agree", "Agree"),
	("Neither Agree nor Disagree", "Neither Agree nor Disagree"),
	("Disagree", "Disagree"),
	("Strongly Disagree", "Strongly Disagree"),
)

SECTION_V_CHOICES = (
	("Definitely Willing", "Definitely Willing"),
	("Probably Willing", "Probably Willing"),
	("Neither Willing nor Unwilling", "Neither Willing nor Unwilling"),
	("Probably Unwilling", "Probably Unwilling"),
	("Definitely Unwilling", "Definitely Unwilling"),
)


class AddPatientForm(forms.ModelForm):
	profile_picture = forms.ImageField(required=False, label='Choose your image')
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=False, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=True, label="Sex", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	BOD = forms.DateField(required=True, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=True, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	contact_number = forms.CharField(required=False, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	alias = forms.CharField(required=False, label="Alias", widget=forms.TextInput(attrs={'placeholder': 'Alias'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	birth_place = forms.CharField(required=True, label="Birth Place", widget=forms.TextInput(attrs={'placeholder': 'Birth Place'}))
	religion = forms.CharField(required=True, label="Religion", widget=forms.TextInput(attrs={'placeholder': 'Religion'}))
	high_education = forms.CharField(required=True, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	citizenship = forms.CharField(required=False, label="Citizenship", widget=forms.TextInput(attrs={'placeholder': 'Citizenship'}))
	nationality = forms.CharField(required=True, label="Nationality", widget=forms.TextInput(attrs={'placeholder': 'Nationality'}))
	workplace = forms.TypedChoiceField(required=True, label="Workplace", choices=WORKPLACE_CHOICES)
	occupation = forms.CharField(required=True, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	employment_status = forms.TypedChoiceField(required=True, label="Employment Status", choices=EMPLOYMENT_STATUS_CHOICES)
	mental_health_history = forms.TypedChoiceField(required=True, label="Mental Health History", choices=YES_NO_TEXT_CHOICES)
	access_to_mental_health = forms.TypedChoiceField(required=True, label="Access To Mental Health", choices=YES_NO_TEXT_CHOICES)
	

	def __init__(self, *args, **kwargs):
		super(AddPatientForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			base_classes = field.widget.attrs.get('class', '')
			css_classes = 'form-control'
			if self.errors.get(field_name):
				css_classes += ' is-invalid'
			field.widget.attrs['class'] = f"{base_classes} {css_classes}".strip()
			

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name', '').strip()
		if not first_name:
			raise forms.ValidationError("First name is required.")
		if not first_name.replace(' ', '').isalpha():
			raise forms.ValidationError("First name should only contain letters and spaces.")
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name', '').strip()
		if not last_name:
			raise forms.ValidationError("Last name is required.")
		if not last_name.replace(' ', '').isalpha():
			raise forms.ValidationError("Last name should only contain letters and spaces.")
		return last_name
	
	# def clean_contact_number(self):
	# 	contact_number = self.cleaned_data.get('contact_number', '').strip()
	# 	if not contact_number.isdigit() or len(contact_number) != 11:
	# 		raise forms.ValidationError("Enter a valid contact number.")
	# 	return contact_number

	def clean_email(self):
		email = self.cleaned_data.get('email', '').strip()
		if email:
			try:
				validate_email(email)
			except forms.ValidationError:
				raise forms.ValidationError("Enter a valid email address.")
		return email

	def clean_BOD(self):
		BOD = self.cleaned_data.get('BOD')
		if BOD and BOD > date.today():
			raise forms.ValidationError("Date of birth cannot be in the future.")
		return BOD

	def clean(self):
		cleaned_data = super().clean()
		first_name = cleaned_data.get('first_name')
		middle_name = cleaned_data.get('middle_name')
		last_name = cleaned_data.get('last_name')
		BOD = cleaned_data.get('BOD')
		if first_name and middle_name and last_name and BOD:
			exists = details.objects.filter(
				first_name__iexact=first_name,
				middle_name__iexact=middle_name,
				last_name__iexact=last_name,
				BOD=BOD
			).exists()
			if exists:
				raise forms.ValidationError("A patient with the same name and date of birth already exists.")
		return cleaned_data

	def patientCheck(self):
		first_name = self.cleaned_data['first_name']
		middle_name = self.cleaned_data['middle_name']
		last_name = self.cleaned_data['last_name']
		BOD = self.cleaned_data['BOD']
		try:
			patient_exists = details.objects.get(first_name=first_name, middle_name=middle_name, last_name=last_name)
			return "Email already present."
		except details.DoesNotExist:
			return False

	def save(self, *args, **kwargs):
		new_patient = details()
		new_patient.profile_picture = self.cleaned_data['profile_picture']
		new_patient.first_name = self.cleaned_data['first_name']
		new_patient.middle_name = self.cleaned_data['middle_name']
		new_patient.last_name = self.cleaned_data['last_name']
		new_patient.gender = self.cleaned_data['gender']
		new_patient.gender_indentity = self.cleaned_data['gender_indentity']
		new_patient.BOD = self.cleaned_data['BOD']
		new_patient.marital_status = self.cleaned_data['marital_status']
		new_patient.contact_number = self.cleaned_data['contact_number']
		new_patient.alias = self.cleaned_data['alias']
		new_patient.email = self.cleaned_data['email']
		new_patient.birth_place = self.cleaned_data['birth_place']
		new_patient.religion = self.cleaned_data['religion']
		new_patient.high_education = self.cleaned_data['high_education']
		new_patient.citizenship = self.cleaned_data['citizenship']
		new_patient.nationality = self.cleaned_data['nationality']
		new_patient.workplace = self.cleaned_data['workplace']
		new_patient.occupation = self.cleaned_data['occupation']
		new_patient.employment_status = self.cleaned_data['employment_status']
		new_patient.mental_health_history = self.cleaned_data['mental_health_history']
		new_patient.access_to_mental_health = self.cleaned_data['access_to_mental_health']
		try:
			new_patient.save()
		except:
			return False
		return new_patient

	class Meta:
		model = details
		fields = ['profile_picture','first_name', 'middle_name', 'last_name', 'gender', 'gender_indentity', 'BOD','marital_status', 'contact_number', 'alias', 'email', 'birth_place', 'religion', 'high_education', 'citizenship', 'nationality', 'workplace', 'occupation', 'employment_status', 'mental_health_history', 'access_to_mental_health']

class EditPatientForm(forms.ModelForm):
	profile_picture = forms.ImageField(required=False, label='Choose your image')
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=False, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=True, label="Sex", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	BOD = forms.DateField(required=True, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=True, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	contact_number = forms.CharField(required=True, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	alias = forms.CharField(required=False, label="Alias", widget=forms.TextInput(attrs={'placeholder': 'Alias'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	birth_place = forms.CharField(required=True, label="Birth Place", widget=forms.TextInput(attrs={'placeholder': 'Birth Place'}))
	religion = forms.CharField(required=True, label="Religion", widget=forms.TextInput(attrs={'placeholder': 'Religion'}))
	high_education = forms.CharField(required=True, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	citizenship = forms.CharField(required=False, label="Citizenship", widget=forms.TextInput(attrs={'placeholder': 'Citizenship'}))
	nationality = forms.CharField(required=True, label="Nationality", widget=forms.TextInput(attrs={'placeholder': 'Nationality'}))
	workplace = forms.TypedChoiceField(required=True, label="Workplace", choices=WORKPLACE_CHOICES)
	occupation = forms.CharField(required=True, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	employment_status = forms.TypedChoiceField(required=True, label="Employment Status", choices=EMPLOYMENT_STATUS_CHOICES)
	mental_health_history = forms.TypedChoiceField(required=True, label="Mental Health History", choices=YES_NO_TEXT_CHOICES)
	access_to_mental_health = forms.TypedChoiceField(required=True, label="Access To Mental Health", choices=YES_NO_TEXT_CHOICES)

	def __init__(self, *args, **kwargs):
		super(EditPatientForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			base_classes = field.widget.attrs.get('class', '')
			css_classes = 'form-control'
			if self.errors.get(field_name):
				css_classes += ' is-invalid'
			field.widget.attrs['class'] = f"{base_classes} {css_classes}".strip()
			

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name', '').strip()
		if not first_name:
			raise forms.ValidationError("First name is required.")
		if not first_name.replace(' ', '').isalpha():
			raise forms.ValidationError("First name should only contain letters and spaces.")
		return first_name
	
	
	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name', '').strip()
		if not last_name.replace(' ', '').isalpha():
			raise forms.ValidationError("Last name should only contain letters and spaces.")
		return last_name
	
	# def clean_contact_number(self):
	# 	contact_number = self.cleaned_data.get('contact_number', '').strip()
	# 	if not contact_number.isdigit() or len(contact_number) !=11:
	# 		raise forms.ValidationError("Enter a valid contact number.")
	# 	return contact_number
	
	def clean_email(self):
		email = self.cleaned_data.get('email', '').strip()
		if email:
			try:
				validate_email(email)
			except forms.ValidationError:
				raise forms.ValidationError("Enter a valid email address.")
		return email
	
	def clean_BOD(self):
		BOD = self.cleaned_data.get('BOD')
		if BOD and BOD > date.today():
			raise forms.ValidationError("Date of birth cannot be in the future.")
		return BOD
	
	def clean(self):
		cleaned_data = super().clean()
		first_name = cleaned_data.get('first_name')
		middle_name = cleaned_data.get('middle_name')
		last_name = cleaned_data.get('last_name')
		BOD = cleaned_data.get('BOD')
		if first_name and middle_name and last_name and BOD:
			# Exclude the current instance when checking for duplicates during editing
			duplicate_query = details.objects.filter(
				first_name__iexact=first_name,
				middle_name__iexact=middle_name,
				last_name__iexact=last_name,
				BOD=BOD
			)
			if self.instance and self.instance.pk:
				duplicate_query = duplicate_query.exclude(pk=self.instance.pk)
			
			if duplicate_query.exists():
				raise forms.ValidationError("A patient with the same name and date of birth already exists.")
		return cleaned_data
	
	def patientCheck(self):
		first_name = self.cleaned_data['first_name']
		middle_name = self.cleaned_data['middle_name']
		last_name = self.cleaned_data['last_name']
		BOD = self.cleaned_data['BOD']
		try:
			patient_exists = details.objects.get(first_name=first_name, middle_name=middle_name, last_name=last_name)
			return "Email already present."
		except:
			return False


	class Meta:
		model = details
		fields = ['profile_picture', 'first_name', 'middle_name', 'last_name', 'gender', 'gender_indentity', 'BOD','marital_status', 'contact_number', 'alias', 'email', 'birth_place', 'religion', 'high_education', 'citizenship', 'nationality', 'workplace', 'occupation', 'employment_status', 'mental_health_history', 'access_to_mental_health']

class AddPatientAddressForm(forms.ModelForm):
	current_street = forms.CharField(required=False, label="Street", widget=forms.TextInput(attrs={'placeholder': 'Street'}))
	current_apt = forms.CharField(required=False, label="apt", widget=forms.TextInput(attrs={'placeholder': 'apt'}))
	current_barangay = forms.CharField(required=False, label="Barangay", widget=forms.TextInput(attrs={'placeholder': 'Barangay'}))
	current_city = forms.CharField(required=False, label="City", widget=forms.TextInput(attrs={'placeholder': 'City'}))
	current_country = forms.CharField(required=False, label="Country", widget=forms.TextInput(attrs={'placeholder': 'Country'}))
	current_province = forms.CharField(required=False, label="Provinces", widget=forms.TextInput(attrs={'placeholder': 'Provinces'}))
	current_zip_code = forms.CharField(required=False, label="Zip Code", widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))

	ph_street = forms.CharField(required=False, label="Street", widget=forms.TextInput(attrs={'placeholder': 'Street'}))
	ph_apt = forms.CharField(required=False, label="apt", widget=forms.TextInput(attrs={'placeholder': 'apt'}))
	ph_barangay = forms.CharField(required=False, label="Barangay", widget=forms.TextInput(attrs={'placeholder': 'Barangay'}))
	ph_city = forms.CharField(required=False, label="City", widget=forms.TextInput(attrs={'placeholder': 'City'}))
	ph_country = forms.CharField(required=False, label="Country", widget=forms.HiddenInput(), initial='Philippines')
	ph_province = forms.CharField(required=False, label="Provinces", widget=forms.TextInput(attrs={'placeholder': 'Provinces'}))
	ph_zip_code = forms.CharField(required=False, label="Zip Code", widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))

	def __init__(self, *args, **kwargs):
		super(AddPatientAddressForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = address
		fields = ['current_street', 'current_apt', 'current_barangay','current_city', 'current_country', 'current_province', 'current_zip_code', 'ph_street', 'ph_apt', 'ph_barangay', 'ph_city', 'ph_country', 'ph_province', 'ph_zip_code']

class EditPatientAddressForm(forms.ModelForm):
	current_street = forms.CharField(required=False, label="Street", widget=forms.TextInput(attrs={'placeholder': 'Street'}))
	current_apt = forms.CharField(required=False, label="apt", widget=forms.TextInput(attrs={'placeholder': 'apt'}))
	current_barangay = forms.CharField(required=False, label="Barangay", widget=forms.TextInput(attrs={'placeholder': 'Barangay'}))
	current_city = forms.CharField(required=False, label="City", widget=forms.TextInput(attrs={'placeholder': 'City'}))
	current_country = forms.CharField(required=False, label="Country", widget=forms.TextInput(attrs={'placeholder': 'Country'}))
	current_province = forms.CharField(required=False, label="Provinces", widget=forms.TextInput(attrs={'placeholder': 'Provinces'}))
	current_zip_code = forms.CharField(required=False, label="Zip Code", widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))

	ph_street = forms.CharField(required=False, label="Street", widget=forms.TextInput(attrs={'placeholder': 'Street'}))
	ph_apt = forms.CharField(required=False, label="apt", widget=forms.TextInput(attrs={'placeholder': 'apt'}))
	ph_barangay = forms.CharField(required=False, label="Barangay", widget=forms.TextInput(attrs={'placeholder': 'Barangay'}))
	ph_city = forms.CharField(required=False, label="City", widget=forms.TextInput(attrs={'placeholder': 'City'}))
	ph_country = forms.CharField(required=False, label="Country", widget=forms.HiddenInput(), initial='Philippines')
	ph_province = forms.CharField(required=False, label="Provinces", widget=forms.TextInput(attrs={'placeholder': 'Provinces'}))
	ph_zip_code = forms.CharField(required=False, label="Zip Code", widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))

	def __init__(self, *args, **kwargs):
		super(EditPatientAddressForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = address
		fields = ['current_street', 'current_apt', 'current_barangay','current_city', 'current_country', 'current_province', 'current_zip_code', 'ph_street', 'ph_apt', 'ph_barangay', 'ph_city', 'ph_country', 'ph_province', 'ph_zip_code']


class AddRelativesForm(forms.ModelForm):
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=False, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=False, label="Sex", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	DOB = forms.DateField(required=False, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=False, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	relationship = forms.TypedChoiceField(required=False, label="Relationship Status", choices=RELATIONSHIP_CHOICES, initial=0)
	high_education = forms.CharField(required=False, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	Workplace = forms.CharField(required=False, label="Workplace", widget=forms.TextInput(attrs={'placeholder': 'Workplace'}))
	occupation = forms.CharField(required=False, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	contact_number = forms.CharField(required=False, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	is_emergency = forms.BooleanField(label='Call incase of Emergency', required=False) 

	def __init__(self, *args, **kwargs):
		super(AddRelativesForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'
		self.fields["is_emergency"].widget.attrs.update({"class": "form-check-input"})


	class Meta:
		model = relatives
		fields = ['first_name', 'middle_name', 'last_name', 'gender', 'gender_indentity', 'DOB', 'marital_status', 'relationship', 'high_education', 'Workplace', 'occupation', 'contact_number', 'email', 'is_emergency']

class EditRelativesForm(forms.ModelForm):
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=False, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=False, label="Sex", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	DOB = forms.DateField(required=False, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=False, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	relationship = forms.TypedChoiceField(required=False, label="Relationship Status", choices=RELATIONSHIP_CHOICES, initial=0)
	high_education = forms.CharField(required=False, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	Workplace = forms.CharField(required=False, label="Workplace", widget=forms.TextInput(attrs={'placeholder': 'Workplace'}))
	occupation = forms.CharField(required=False, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	contact_number = forms.CharField(required=False, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	is_emergency = forms.BooleanField(label='Call incase of Emergency', required=False) 

	def __init__(self, *args, **kwargs):
		super(EditRelativesForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'
		self.fields["is_emergency"].widget.attrs.update({"class": "form-check-input"})

	class Meta:
		model = relatives
		fields = ['first_name', 'middle_name', 'last_name', 'gender', 'gender_indentity', 'DOB', 'marital_status', 'relationship', 'high_education', 'Workplace', 'occupation', 'contact_number', 'email', 'is_emergency']


class patientSurveyForm(forms.ModelForm):

	social_phobia = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	generalized_anxiety_disorder = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	major_depressive_disorder = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	disorder_personality_disorder = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	dysthymia = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	agoraphobia = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	bipolar_disorder = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	drug_dependence = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	mas_babae = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	mas_lalake = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)

	kalidad_pagtulog = forms.TypedChoiceField(required=True, choices=SECTION_II_CHOICES, widget=forms.RadioSelect)
	iwasan_aktibidad = forms.TypedChoiceField(required=True, choices=SECTION_II_CHOICES, widget=forms.RadioSelect)

	cognitive_behavior_therapy = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	kumpidensyal = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	hindi_nagbabanta = forms.TypedChoiceField(required=True, choices=SECTION_I_CHOICES, widget=forms.RadioSelect)
	
	hahanapin_impormasyon_sakit_isip = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	humingi_impormasyon_sakit_isip = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	pagpapatingin_sa_doktor = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	mapagkukunan_impormasyon_sakit_isip = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	bumalik_tamang_kaisipan = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	personal_kahinaan = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	sakit_medikal = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	mapanganib = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	umiwas_taong_sakit_isip = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	hindi_sasabihin_kahit_kanino = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	question_26 = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	question_27 = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)
	hindi_magiging_epektibo = forms.TypedChoiceField(required=True, choices=SECTION_IV_CHOICES, widget=forms.RadioSelect)

	lumipat_ng_bahay = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	pakikisalamuha_isang_taong = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	question_31 = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	question_32 = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	question_33 = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	question_34 = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)
	question_35 = forms.TypedChoiceField(required=True, choices=SECTION_V_CHOICES, widget=forms.RadioSelect)

	

	def __init__(self, *args, **kwargs):
		super(patientSurveyForm, self).__init__(*args, **kwargs)


	class Meta:
		model = patient_survey
		fields = ['social_phobia', 'generalized_anxiety_disorder', 'major_depressive_disorder', 'disorder_personality_disorder', 'dysthymia', 'agoraphobia', 'bipolar_disorder', 'drug_dependence', 'mas_babae', 'mas_lalake', 'kalidad_pagtulog', 'iwasan_aktibidad', 'cognitive_behavior_therapy', 'kumpidensyal', 'hindi_nagbabanta', 'hahanapin_impormasyon_sakit_isip', 'humingi_impormasyon_sakit_isip', 'pagpapatingin_sa_doktor', 'mapagkukunan_impormasyon_sakit_isip', 'bumalik_tamang_kaisipan', 'personal_kahinaan', 'sakit_medikal', 'mapanganib', 'umiwas_taong_sakit_isip', 'hindi_sasabihin_kahit_kanino', 'question_26', 'question_27', 'hindi_magiging_epektibo', 'lumipat_ng_bahay', 'pakikisalamuha_isang_taong', 'question_31', 'question_32', 'question_33', 'question_34', 'question_35']


class patientFilesForm(forms.ModelForm):
	file_name = forms.CharField(required=True, label="File Name", widget=forms.TextInput(attrs={'placeholder': 'File Name'}))
	file = forms.FileField(required=True, label='Choose your File')

	def __init__(self, *args, **kwargs):
		super(patientFilesForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'


	class Meta:
		model = details_files
		fields = ['file_name', 'file']

def formatDate(dateValue):
	current_date_split = dateValue.split("/")
	if len(current_date_split) == 3:
		return current_date_split[2]+"-"+current_date_split[0]+"-"+current_date_split[1]
	else:
		return False

		