from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SwimSpot, SavedSwims, User, Comment, Photo, Location, UserProfile

admin.site.register(SwimSpot)
admin.site.register(SavedSwims)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Location)
admin.site.register(UserProfile)

#can add more admins & change look of admin site, list config etc, add list filters https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site