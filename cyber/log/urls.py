
from django.urls import path
from . import views
urlpatterns = [
    path ('login/', views.login_user, name="login"),
    path ('logout/', views.logout_user, name="logout"),
    path ('register/', views.registerPage, name="register"),
    path ('scan/', views.scaning, name="scan"),
    path ('scan_result/', views.scan_result, name="scan"),
 ]