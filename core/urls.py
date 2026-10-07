from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_donor, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    path("donors/", views.search_donors, name="search_donors"),
    path("about/", views.about, name="about"),
]
