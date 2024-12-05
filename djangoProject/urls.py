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
from login.views import sinup,login,home,dashboard,logout,upload,note_list,feedback,forgot_password,password_reset_sent,reset_password, verify_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sinup/',sinup,name='sinup'),
    path('login/',login,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout',logout,name='logout'),
    path('',home,name='home'),
    path('upload/', upload, name='upload'),  # URL for note upload (restricted to lecturers)
    path('note_list/',note_list,name='note_list'),
    path('feedback/',feedback,name='feedback'),

    path('forgot_password', forgot_password ,name='forgot_password'),
    path('password_reset_sent/<str:reset_id>/', password_reset_sent, name='password_reset_sent'),
    path('reset_password/<str:reset_id>/', reset_password,name="reset_password"),
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)