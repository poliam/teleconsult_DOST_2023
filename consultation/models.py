from django.db import models

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

	