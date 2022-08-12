from cProfile import Profile
from django.shortcuts import render, redirect
import requests
import json 
from itertools import chain
from .models import SwimSpot, SavedSwims, Comment, User, SwimForm, Photo, PhotoForm, Location, FilterForm, UserProfile, UPForm, ProfilePic, PicForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timezone, timedelta
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator


def index(request):
    form = ""
    if request.method == 'POST':
        f = FilterForm(request.POST)
        filter_parameters = {}
        if f.is_valid():
            for item in ['distance_suitable', 'cafe', 'toilets']:
                if f.cleaned_data.get(item) is True:
                    filter_parameters[item] = True
            swimspots = SwimSpot.objects.filter(**filter_parameters)
            form = None          
    else:
        form = FilterForm()
        swimspots = SwimSpot.objects.all().order_by('id') #gets all swimspots 
    vals = swimspots.values_list('id', 'name', 'water_quality', 'is_approved', 'description')
    listo = []
    for item in vals:
        henlo = list(Photo.objects.filter(swim_id=item[0])[:1])
        objects = list(chain(item, henlo))
        listo.append(objects)
    paginator = Paginator(listo, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    return render(request, "index.html", {
        "swimspots": swimspots,
        "form": form,
        "page_obj": page_obj
    })


def pages(request):
    posts = SwimSpot.objects.all()
    paginator = Paginator(posts, 3)
    page_obj = paginator.get_page(1)
    page_number = request.GET.get('page', 1)
    pge = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page_obj': page_obj,
    })

@csrf_protect
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return index(request)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return index(request)
    else:
        return render(request, "register.html")


def update_water_quality(request, wqid):
    url = 'https://environment.data.gov.uk/doc/bathing-water/{0}.json'.format(wqid)
    print("this is wqid", wqid)
    swim = SwimSpot.objects.get(wq_id=wqid)
    response = requests.get(url)
    if response.status_code != 200:
        swim.water_quality = "Sorry, water quality data for this swim location is not currently available"
        swim.save()
        return render(request, "swimspot.html", {})  
    else:  
        data = response.json()  
        swim.water_quality = data['result']['primaryTopic']['latestComplianceAssessment']['complianceClassification']['name']['_value']
        swim.save()
    return render(request, "swimspot.html", {})    
    #the function can take water quality id as input
    #take wqid and insert into url string to request data. 
    #filter swimspot objects by wqid and update the water quality accordingly. 
    #if data is None, model value can be saved as "sorry, data unavailable"
    

def get_swim_spot(request, id):  
    swim = SwimSpot.objects.filter(id=id)
    swims = swim.values_list('id', 'name', 'description', 'toilets', 'cafe', 'water_quality', 'distance_suitable')
    water_quality = swim.values_list('wq_id', flat=True)
    print("water quality", water_quality[0])
    update_water_quality(request, water_quality[0])
    commentos = Comment.objects.filter(swim_id=id).order_by('-date_added')
    phot = Photo.objects.filter(swim_id=id)
    location = list(Location.objects.filter(swimspot=id).order_by('name').values())
    location_json = json.dumps(location)
    swimmo = SavedSwims.objects.filter(user=request.user).filter(swim_id=id)
    print("swimmo", swimmo)
    saved = swimmo.values_list('swim_id')
    print("saved zero", saved)
    return render(request, "swimspot.html", {
        "phot": phot,
        "swims": swims,
        "locations": location_json,
        "commentos": commentos,
        "saved": saved
    })    
 

def search(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = SwimSpot.objects.filter(name__contains=query_name)
            return render(request, 'search.html', {"results":results})

    return render(request, 'search.html')

def view_on_map(request):
    location_list = list(Location.objects.order_by('name').values()) 
    location_json = json.dumps(location_list)  
    context = {'locations': location_json} 
    return render(request, 'mapview.html', context) 


@login_required()
def add_listing(request):
    form = ""
    if request.method == 'POST':
        s = SwimForm(request.POST)
        swimmy = SwimSpot()
        if s.is_valid():
            swimmy.added_by = request.user #is there a need to store this data?
            swimmy.name = s.cleaned_data.get('name')
            swimmy.description = s.cleaned_data.get('description')
            swimmy.toilets = s.cleaned_data.get('toilets')
            swimmy.cafe = s.cleaned_data.get('cafe')
            swimmy.save()
            id = swimmy.id
            return render(request, 'thankyou.html', {'id':id})
    else:
        form = SwimForm()
    return render(request, 'addlisting.html', {'form': form,
    })


@login_required()
def save_swim(request, id):
        this = SwimSpot.objects.get(id=id)
        saved = SavedSwims.objects.filter(user=request.user).filter(swim_id=id)
        scount = False    
        if saved.count() > 0:
            scount = True 
        ifsaved = {
        'scount': scount }
        if saved:
            saved.delete()
        else:    
            swi = SavedSwims()
            swi.user = request.user
            swi.swim_id = this
            swi.save()
        return JsonResponse({"ifsaved": ifsaved}, status=200)  #this is supposed to serialise the boolean and send it to the page 

@login_required()
def get_saved_swims(request, id):
    swimmo = SavedSwims.objects.filter(user=request.user) #change this to take in a parameter that reflects users id
    saved_swims = swimmo.values_list('user', 'swim_id')

    
    return render(request, "saved.html", {
        "saved_swims": saved_swims
    })


@login_required()
def comment(request, id):
    if request.method == 'POST':     
        this = SwimSpot.objects.get(id=id)
        commentie = Comment()
        commentie.comment = request.POST.get('comment')
        commentie.user = request.user
        commentie.swim_id = this
        commentie.save()
        return redirect('get', id=id)


@login_required()
def add_photo(request, id):
    this = SwimSpot.objects.get(id=id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        photo = Photo()
        if form.is_valid():
            photo.swim_id = this
            photo.title = form.cleaned_data.get('title')
            photo.description = form.cleaned_data.get('description')
            photo.image = form.cleaned_data.get('image')
            photo.submitter_id = request.user.id
            photo.save()
            if photo.swim_id.is_approved == True:
                return redirect('get', id=id)
            else: 
                return render(request, "submitted.html")    
    else:
        form = PhotoForm()
    return render(request, 'create.html', {'form': form,
    'this' : this
    })
  

def get_profile(request, id):
    form = PicForm()
    u1 = User.objects.get(id=id)
    try:
        swimmo = SavedSwims.objects.filter(user=u1)
    except SavedSwims.DoesNotExist:
        swimmo = None
    if swimmo is not None:
        saved_swims = swimmo.values_list('user', 'swim_id')
      
    try:
        photo = ProfilePic.objects.get(user_id=u1)
    except ProfilePic.DoesNotExist:
        photo = None     
    try:   
        prof = UserProfile.objects.filter(pk=u1)
    except UserProfile.DoesNotExist:
        prof = None 
    if prof.count() == 0:
        if request.user == u1:
            return edit_profile(request, id)   
        else:
            return render(request, 'notfound.html')  
    print(saved_swims)         
    return render(request, 'profilepage.html', {'prof': prof,
    'form': form,
    'photo': photo,
    'saved_swims': saved_swims,
    'swimmo': swimmo})

def edit_profile(request, id):
    prof = UserProfile()
    u1 = User.objects.get(id=id)
    content = UserProfile.objects.filter(pk=u1)
    if request.method == 'GET':
        if content.count() == 0:
            formie = UPForm()
        else:    
            formie = UPForm({'events_completed': content[0].events_completed,
            "blurb": content[0].blurb,
            "training_for": content[0].training_for
        })
    else: 
        profile = UPForm(request.POST) 
        if profile.is_valid():
            content.delete() #deletes existing user profile
            prof.user = request.user
            prof.events_completed = profile.cleaned_data["events_completed"]
            prof.blurb = profile.cleaned_data["blurb"]
            prof.training_for = profile.cleaned_data["training_for"]
            prof.save()
        return get_profile(request, id)    
    return render(request, 'editprofile.html', {
        'content' : content,
        'form' : formie,
        'u1'   : u1
    })

def all_photos(request, id):   
    phot = Photo.objects.filter(swim_id=id)
    photo = phot.values_list('image')
    return render(request, 'allphotos.html', {
        'photo': photo
    })

def add_profile_pic(request, id):
    u1 = User.objects.get(id=id) # retrieves user model 
    id = u1.id # gets user id from above model
    
    beb = str(id)
    url = '../profile/' + beb
    

    if request.method == 'POST':   
        pic_f = PicForm(request.POST, request.FILES)   
        try: 
            existing = ProfilePic.objects.get(pk=id)
            existing.delete()   #deletes the old profile pic
            if pic_f.is_valid():
                new_pp = ProfilePic()
                new_pp.user_id = request.user.id
                new_pp.image = pic_f.cleaned_data["image"]
                new_pp.save()
                return HttpResponseRedirect(url)
        except ProfilePic.DoesNotExist:
            if pic_f.is_valid():
                new_pp = ProfilePic()
                new_pp.user_id = request.user.id
                new_pp.image = pic_f.cleaned_data["image"]
                new_pp.save()
                return HttpResponseRedirect(url)

