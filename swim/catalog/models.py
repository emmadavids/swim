from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.forms import ModelForm
from datetime import datetime, timezone, timedelta
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset


class User(AbstractUser):
    pass


class SwimSpot(models.Model):
    name = models.CharField(max_length=100, default='name')
    description = models.CharField(max_length=1440, default='', null=True, blank=True)
    #photo = https://www.sitepoint.com/django-photo-sharing-app/ - photo CRUD tutorial can have one to one relationship with photo model 
    #location- code this later
    water_quality = models.CharField(max_length=100, default='', null=True, blank=True)
    #User rating?????
    toilets = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    #fresh or sea water? 
    #suitable for distance training? 
    is_approved = models.BooleanField(default=False) #admin can approve 
    wq_id = models.CharField(max_length=100, default='', null=True, blank=True)
 
    def __str__(self):
        return f"{self.name} : {self.description}"  


class SwimForm(ModelForm):
    class Meta:
        model = SwimSpot
        fields = ['name', 'description', 'toilets', 'cafe'] #add photo


class SavedSwims(models.Model):
    user = models.CharField(max_length=25, default="string", null=True, blank=True)
    swim_id = models.CharField(max_length=100, default="swim_id")
    def __str__(self):
        return f"{self.user} | {self.swim_id}"    


class Comment(models.Model):
    user = models.CharField(max_length=25, default="string", null=True, blank=True)
    swim_id = models.CharField(max_length=100, default='0')
    date_added = models.DateTimeField(max_length=64, default=datetime.now(timezone.utc))
    comment = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.user} : {self.comment}"        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class Photo(models.Model):

    swim_id = models.CharField(max_length=100, default='0')

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250) 

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'title',
                'description',
                'image',
            )
        )   

class Location(models.Model)

#Remember to register new models to admin
