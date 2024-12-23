from django.contrib import admin

# Register your models here.
from .models import Student,Profile,Note,Feedback,PasswordReset,Subject,Number
admin.site.register(Note)
admin.site.register(Feedback)
admin.site.register(PasswordReset)
admin.site.register(Subject)
admin.site.register(Number)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'category', 'registration_number')

