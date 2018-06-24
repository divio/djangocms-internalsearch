from django.views.generic import TemplateView
# from django.shortcuts import render_to_response

class SearchView(TemplateView):
    template_name = "djangocms_internalsearch/index.html"
