"""easy_hostel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from easy_hostel import settings
from .import views as easy_hostel_view
import student.views
import warden.views
import admin_app.views

urlpatterns = [
    path('', easy_hostel_view.home, name='home'),
    path('', include('student.urls')),
    path('', include('warden.urls')),
    path('', include('admin_app.urls')),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
