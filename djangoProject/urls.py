"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from login.views import sinup,login,home,dashboard,logout,upload,note_list,feedback,forgot_password,password_reset_sent,reset_password, verify_email,delete_note,subject_list,download_note,profile_view
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sinup/',sinup,name='sinup'),
    path('login/',login,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout',logout,name='logout'),
    path('',home,name='home'),
    path('upload/', upload, name='upload'),  # URL for note upload (restricted to lecturers)
    path('feedback/',feedback,name='feedback'),
    path('delete-note/<int:note_id>/', delete_note, name='delete_note'),
    path('forgot_password', forgot_password ,name='forgot_password'),
    path('password_reset_sent/<str:reset_id>/', password_reset_sent, name='password_reset_sent'),
    path('reset_password/<str:reset_id>/', reset_password,name="reset_password"),
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('subjects', subject_list, name='subject_list'),
    path('subject/<int:subject_id>/notes/', note_list, name='note_list'),
    path('download/<int:note_id>/',download_note, name='download_note'),
    path('profile/',profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        success_url='/password-change/done/'
    ), name='password_change'),

    # Password change done page
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),


]
