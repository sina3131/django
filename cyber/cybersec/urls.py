from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index , name="index"),
    path('home/', views.home , name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("django.contrib.auth.urls")), 
    
    
]