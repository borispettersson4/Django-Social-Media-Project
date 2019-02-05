from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Topic)
admin.site.register(Activity)
admin.site.register(Notification)
admin.site.register(Request)
# Register your models here.
