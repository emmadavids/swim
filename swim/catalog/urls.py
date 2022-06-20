from django.urls import path
from . import views
from django.contrib.auth import views as v

# app_name = 'photo'

urlpatterns = [
 path('', views.index, name='index'),
 path(r'^login/', views.login_view, name="login"),
 path(r'^logout/', views.logout_view, name="logout"),
 path('catalog/login/', v.LoginView.as_view(), name="login"),
 path('catalog/logout/',v.LogoutView.as_view(next_page='/'),name="logout"),
 path("register", views.register, name="register"),
 path("<int:id>/", views.get_swim_spot, name="get"),
 path("comment/<int:id>", views.comment, name="comment"),
 path("add/", views.add_listing, name="add"),
 path("save_swim/<int:id>/", views.save_swim, name="save_swim"),
 path("getswims/", views.get_saved_swims, name="getswims"),
 path('search', views.search, name = "search"),
 path('addphoto/<int:id>/', views.add_photo, name='addphoto'),
 path('map', views.view_on_map, name='map'),
 path("profile/<int:id>", views.get_profile, name='profile'),
 path("addpic/<int:id>", views.add_profile_pic, name='picadd'),
 path("edit/<int:id>", views.edit_profile, name='edit'),    
 path("allpix/<int:id>", views.all_photos, name='allpix'), 

 
#  path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),
]

