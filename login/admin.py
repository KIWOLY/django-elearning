from django.contrib import admin

# Register your models here.
from .models import Student,Profile,Note,Feedback,PasswordReset
admin.site.register(Profile)
admin.site.register(Note)
admin.site.register(Feedback)
admin.site.register(PasswordReset)


