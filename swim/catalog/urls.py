from django.urls import path
from . import views

# app_name = 'photo'

urlpatterns = [
 path('', views.index, name='index'),
 path("login", views.login_view, name="login"),
 path("logout", views.logout_view, name="logout"),
 path("register", views.register, name="register"),
 path("<int:id>/", views.get_swim_spot, name="get"),
 path("comment/<int:id>", views.comment, name="comment"),
 path("add/", views.add_listing, name="add"),
 path("swims/<int:id>", views.save_swim, name="save_swim"),
 path("getswims/", views.get_saved_swims, name="getswims"),
 path("search", views.search, name="search"),
 path('success', views.success, name = 'success'),
 path('addphoto/<int:id>/', views.add_photo, name='addphoto'),
 path('map', views.view_on_map, name='map'),
#  path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),
]

