from django.conf.urls import url
from . import views

urlpatterns = [
    url('signup$', views.NewUser.as_view()),
    url('login$', views.Login.as_view()),
    url('logout$', views.Logout.as_view()),
    url('infection/submit$', views.SubmitInfectionData.as_view()),
]
