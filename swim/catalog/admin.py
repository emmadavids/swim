from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SwimSpot, SavedSwims, User, Comment, Photo 

admin.site.register(SwimSpot)
admin.site.register(SavedSwims)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Photo)

#can add more admins & change look of admin site, list config etc, add list filters https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site