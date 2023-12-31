from django.db import models

# Create your models here.
class details(models.Model):
	first_name = models.CharField(max_length=250, null=True, blank=True)
	middle_name = models.CharField(max_length=250, null=True, blank=True)
	last_name = models.CharField(max_length=250, null=True, blank=True)
	gender = models.CharField(max_length=250, null=True, blank=True)
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
	profile_picture = models.FileField(upload_to='profile_photo/', null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	history = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)

class address(models.Model):
	street = models.CharField(max_length=250, null=True, blank=True)
	apt = models.CharField(max_length=250, null=True, blank=True)
	barangay = models.CharField(max_length=250, null=True, blank=True)
	province = models.CharField(max_length=250, null=True, blank=True)
	city = models.CharField(max_length=250, null=True, blank=True)
	country = models.CharField(max_length=250, null=True, blank=True)
	zip_code = models.CharField(max_length=250, null=True, blank=True)
	is_current = models.BooleanField(default=1)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=1)
	is_delete = models.BooleanField(default=0)
	details = models.ForeignKey(details, null=True, blank=True, on_delete=models.SET_NULL,)
	