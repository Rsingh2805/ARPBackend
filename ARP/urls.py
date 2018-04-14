from django.conf.urls import url
from . import views

urlpatterns = [
    url('signup$', views.NewUser.as_view()),
    url('login$', views.Login.as_view()),
    url('logout$', views.Logout.as_view()),
    url('infection/submit$', views.SubmitInfectionData.as_view()),
    url('infection/history$', views.GetInfectionHistory.as_view()),
    url('user/profile$', views.GetUserProfile.as_view()),
    url('infection/fixed$', views.BreachFixed.as_view()),
]
