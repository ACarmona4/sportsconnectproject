"""
URL configuration for SportsConnect project.

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
from django.contrib import admin
from django.urls import path
from reservation import views as reservationViews

from django.conf.urls.static import static
from django.conf import settings
from reservation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',reservationViews.home),
    path('get_availability_by_date/', reservationViews.get_availability_by_date, name='get_availability_by_date'),
    path('reservate/', reservationViews.reservate, name='reservate'),
    path('delete_reservation/', views.delete_reservation, name='delete_reservation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)