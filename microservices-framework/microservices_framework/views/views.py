from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import TemplateView

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
