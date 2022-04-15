from django.shortcuts import render

# Create your views here.
from django.views import generic as views


class ContactView(views.TemplateView):
    template_name = 'contacts/contacts.html'
