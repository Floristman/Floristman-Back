from django.urls import path
from .views import *


urlpatterns = [
    path("", sign_up, name="sign-up"),
    path("login/", sign_in, name="sign-in"),
    path("logout/", sign_out, name="sign-out"),
]






