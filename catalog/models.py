from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.forms import ModelForm
from datetime import datetime, timezone, timedelta
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from cloudinary.models import CloudinaryField



class User(AbstractUser):
    pass


class SwimSpot(models.Model):
    name = models.CharField(max_length=100, default='name')
    description = models.CharField(max_length=1440, default='', null=True, blank=True)
    water_quality = models.CharField(max_length=100, default='', null=True, blank=True)
    #User rating?????
    toilets = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    #fresh or sea water? 
    distance_suitable = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False) #admin can approve 
    wq_id = models.CharField(max_length=100, default='', null=True, blank=True)
 

    def __str__(self):
        return f"{self.name} : {self.description}"  

class FilterForm(forms.ModelForm):
    distance_suitable = forms.BooleanField(required=False)
    toilets = forms.BooleanField(required=False)
    cafe = forms.BooleanField(required=False)
    class Meta:
        model = SwimSpot
        fields = ['distance_suitable', 'toilets', 'cafe']

class SwimForm(ModelForm):
    class Meta:
        model = SwimSpot
        fields = ['name', 'description', 'toilets', 'cafe'] #add photo


class SavedSwims(models.Model):
    user = models.CharField(max_length=25, default="string", null=True, blank=True)
    swim_id = models.ForeignKey(
        SwimSpot,
        default=1,
        on_delete=models.CASCADE
    ) 
    def __str__(self):
        return f"{self.user} | {self.swim_id}"    


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_added = models.DateTimeField(max_length=64, default=datetime.now(timezone.utc))
    comment = models.CharField(max_length=500)
    swim_id = models.ForeignKey(
        SwimSpot,
        default=1,
        on_delete=models.CASCADE,
    ) 
    hello = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.comment}"        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class Photo(models.Model):
    swim_id = models.ForeignKey(
        SwimSpot,
        default=1,
        on_delete=models.CASCADE,
        related_name="swimspot"
    ) 
    description = models.CharField(max_length=250) 
    created = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['description', 'image']
    
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

class Location(models.Model):
   name = models.CharField(max_length=250) 
   address = models.TextField() 
   latitude = models.FloatField() 
   longitude = models.FloatField() 
   swimspot  = models.OneToOneField(
        SwimSpot,
        default=1,
        on_delete=models.CASCADE
    ) 

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    events_completed = models.CharField(max_length=500) 
    training_for = models.CharField(max_length=500) 
    blurb = models.CharField(max_length=500) 




class UPForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['events_completed', 'training_for', 'blurb']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'events_completed',
                'training_for',
                'blurb',
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )

class ProfilePic(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    image = CloudinaryField('image')


class PicForm(ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['image']    


