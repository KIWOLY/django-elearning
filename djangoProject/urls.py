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
from login.views import sinup,login,home,dashboard,logout,upload,note_list,feedback,password_reset
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
    path('password_reset',password_reset, name='password_reset'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)