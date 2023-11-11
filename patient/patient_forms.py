from django import forms
from patient.models import details, address, relatives, medicine, allergies, global_psychotrauma_screen, considering_event, hamd

SEX_CHOICES = (
	(0, "- - Select Sex - -"),
    ("Male", "Male"),
    ("Female", "Female")
)

YES_NO_CHOICES = [
	(0, "No"), 
	(1, "Yes")
]

MARITAL_CHOICES = (
	("0", "- - Select Status - -"),
	("Single", "Single"),
	("Married", "Married"),
	("Widowed", "Widowed"),
	("Divorced", "Divorced"),
	("Separated", "Separated"),
	("Registered Partnership", "Registered Partnership"),
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

class AddRelativesForm(forms.ModelForm):
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=True, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=False, label="Gemder", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	DOB = forms.DateField(required=False, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=False, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	relationship = forms.TypedChoiceField(required=False, label="Relationship Status", choices=RELATIONSHIP_CHOICES, initial=0)
	high_education = forms.CharField(required=False, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	Workplace = forms.CharField(required=False, label="Workplace", widget=forms.TextInput(attrs={'placeholder': 'Workplace'}))
	occupation = forms.CharField(required=False, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	contact_number = forms.CharField(required=False, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	is_emergency = forms.BooleanField(label='Call incase of Emergency') 

	def __init__(self, *args, **kwargs):
		super(AddRelativesForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			try:
				visible.field.widget.attrs['class'] = 'form-control '+ str(visible.field.widget.attrs['class'])
			except:
				visible.field.widget.attrs['class'] = 'form-control'
		self.fields["is_emergency"].widget.attrs.update({"class": "form-check-input"})

	def save(self, request, patient_instance, *args, **kwargs):
		new_relatives = relatives()
		new_relatives.first_name = request.POST['first_name']
		new_relatives.middle_name = request.POST['middle_name']
		new_relatives.last_name = request.POST['last_name']
		new_relatives.gender = request.POST['gender']
		new_relatives.gender_indentity = request.POST['gender_indentity']
		new_relatives.DOB = formatDate(request.POST['DOB']) 
		new_relatives.marital_status = request.POST['marital_status']
		new_relatives.relationship = request.POST['relationship']
		new_relatives.high_education = request.POST['high_education']
		new_relatives.Workplace = request.POST['Workplace']
		new_relatives.occupation = request.POST['occupation']
		new_relatives.contact_number = request.POST['contact_number']
		new_relatives.email = request.POST['email']
		new_relatives.details = patient_instance

		try:
			new_relatives.save()
		except:
			return False

		return new_relatives.pk


	class Meta:
		model = relatives
		fields = ['first_name', 'middle_name', 'last_name', 'gender', 'gender_indentity', 'DOB', 'marital_status', 'relationship', 'high_education', 'Workplace', 'occupation', 'contact_number', 'email', 'is_emergency']

class EditRelativesForm(forms.ModelForm):
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	middle_name = forms.CharField(required=True, label="Middle Name", widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	gender = forms.TypedChoiceField(required=False, label="Gemder", choices=SEX_CHOICES, initial=0)
	gender_indentity = forms.CharField(required=False, label="Gender Identity", widget=forms.TextInput(attrs={'placeholder': 'Gender Identity'}))
	DOB = forms.DateField(required=False, label="Date of Birth(mm/dd/yyyy)", widget=forms.DateInput(format="%m/%d/%Y"), input_formats=("%m/%d/%Y",))
	marital_status = forms.TypedChoiceField(required=False, label="Marital Status", choices=MARITAL_CHOICES, initial=0)
	relationship = forms.TypedChoiceField(required=False, label="Relationship Status", choices=RELATIONSHIP_CHOICES, initial=0)
	high_education = forms.CharField(required=False, label="Highest Education Attainment", widget=forms.TextInput(attrs={'placeholder': 'Highest Education Attainment'}))
	Workplace = forms.CharField(required=False, label="Workplace", widget=forms.TextInput(attrs={'placeholder': 'Workplace'}))
	occupation = forms.CharField(required=False, label="Occupation", widget=forms.TextInput(attrs={'placeholder': 'Occupation'}))
	contact_number = forms.CharField(required=False, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
	email = forms.CharField(required=False, label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	is_emergency = forms.BooleanField(label='Call incase of Emergency') 

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

def formatDate(dateValue):
	current_date_split = dateValue.split("/")
	if len(current_date_split) == 3:
		return current_date_split[2]+"-"+current_date_split[0]+"-"+current_date_split[1]
	else:
		return False

		