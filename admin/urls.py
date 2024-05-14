from django.urls import path

from . import views

urlpatterns = [
    path("identities", views.IdentityCreateView.as_view(), name="identity-create"),
]
