"""microservices_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path, re_path

from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage

from microservices_framework.views import views
from microservices_framework.views import services

from vyperlogix.django.django_utils import get_optionals


optionals = get_optionals(services.RestServicesAPI.as_view(), num_url_parms=int(os.environ.get('NUM_URL_PARMS', 10)))

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),

    path('rest/services/<slug:func>/', include(optionals) ),
    path('rest/services/<slug:module>/<slug:func>/', include(optionals) ),
    
    url(r'^$', views.Home.as_view()),
]

