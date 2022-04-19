from django.shortcuts import render, redirect
import requests
from .models import SwimSpot, SavedSwims, Comment, User, SwimForm, Photo, PhotoForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timezone, timedelta
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import HttpResponse


def index(request):
    swimspots = SwimSpot.objects.all().order_by('id') #gets all swimspots 
    return render(request, "index.html", {
        "swimspots": swimspots,
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
    response = requests.get(url)
    data = response.json()
    swim = SwimSpot.objects.get(wq_id=wqid)
    print("water quality data :", data['result']['primaryTopic']['latestComplianceAssessment']['complianceClassification']['name']['_value'])
    if data is None:
        swim.water_quality = "Sorry, water quality data for this swim location is not available"
        swim.save()
    else:    
        swim.water_quality = data['result']['primaryTopic']['latestComplianceAssessment']['complianceClassification']['name']['_value']
        swim.save()
    return render(request, "swimspot.html", {})    
    #the function can take water quality id as input
    #take wqid and insert into url string to request data. 
    #filter swimspot objects by wqid and update the water quality accordingly. 
    #if data is None, model value can be saved as "sorry, data unavailable"
    

def get_swim_spot(request, id):  
    swim = SwimSpot.objects.filter(id=id)
    swims = swim.values_list('id', 'name', 'description', 'toilets', 'cafe', 'water_quality')
    water_quality = swim.values_list('wq_id', flat=True)
    print(water_quality[0])
    update_water_quality(request, water_quality[0])
    commentos = Comment.objects.filter(swim_id=id)
    comments = commentos.values_list('user', 'comment', 'id', 'date_added')
    phot = Photo.objects.filter(swim_id=id)
    photo = phot.values_list('image')
    return render(request, "swimspot.html", {
        "photo": photo,
        "swims": swims,
        "comments": comments
    })    


def search(request):
    # swimmo = SavedSwims.objects.filter(user=request.user.id)
    # saved_swims = swimmo.values_list('user', 'swim_id')
    return render(request, "search.html", {
       
    })


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
            return index(request)
    else:
        form = SwimForm()
    return render(request, 'addlisting.html', {'form': form,
    })


@login_required()
def save_swim(request, id):
        this = SwimSpot.objects.get(id=id)
        swi = SavedSwims()
        swi.user = request.user.id
        swi.swim_id = this.id
        swi.save()
        return redirect('getswims') #save swims html still needs to be made 

@login_required()
def get_saved_swims(request):
    swimmo = SavedSwims.objects.filter(user=request.user.id)
    saved_swims = swimmo.values_list('user', 'swim_id')
    return render(request, "saved.html", {
        "saved_swims": saved_swims
    })


@login_required()
def comment(request, id):
    if request.method == 'POST':     
        this = SwimSpot.objects.get(id=id)
        print("this should be the listing id", this.id)
        commentie = Comment()
        commentie.comment = request.POST.get('comment')
        commentie.user = request.user.username
        commentie.swim_id = int(this.id)
        print("fdhjfd: ", commentie.swim_id)
        commentie.save()
        return redirect('get', id=id)



@login_required()
def add_photo(request, id):
    this = SwimSpot.objects.get(id=id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        photo = Photo()
        if form.is_valid():
            # swimmy.added_by = request.user #is there a need to store this data?
            photo.swim_id = int(this.id)
            photo.title = form.cleaned_data.get('title')
            photo.description = form.cleaned_data.get('description')
            photo.image = form.cleaned_data.get('image')
            photo.submitter_id = request.user.id
            photo.save()
            return redirect('get', id=id)
    else:
        form = PhotoForm()
    return render(request, 'create.html', {'form': form,
    })
  
def success(request):
    return HttpResponse('successfully uploaded')


