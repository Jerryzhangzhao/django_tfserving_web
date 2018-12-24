from django.conf.urls import url
from django.contrib import admin
from . import search

urlpatterns = [
    url(r'^search-form$', search.search_form),
    url(r'^search$', search.search),
]
