from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("upload/", views.upload , name="upload"),
    path("marksheets", views.marksheets, name="marksheets")

    
]
