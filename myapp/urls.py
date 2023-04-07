
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("home/",views.hello),
    path("projects/",views.projects),
    path("form/",views.form)
]
