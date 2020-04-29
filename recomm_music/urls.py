from django.urls import path
from . import views

urlpatterns = [
    path('', views.recomm_link),

]