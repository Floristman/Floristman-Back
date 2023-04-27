from django.urls import path

from api.v1.auth.views import LoginViev, RegisView, StepOne, StepTwo, LikeDislike
from api.v1.basket.views import BasketView

urlpatterns = [
    path('login/', LoginViev.as_view()),
    path('regis/', RegisView.as_view()),
    path('stepone/', StepOne.as_view()),
    path('steptwo/', StepTwo.as_view()),
    path('basket/', BasketView.as_view()),
    path('like/', LikeDislike.as_view())
]
