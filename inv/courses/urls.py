from django.urls import path
from . import views

urlpatterns = [
    path('inv/', views.site),
]
