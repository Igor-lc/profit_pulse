from django.urls import path
from . import views

urlpatterns = [
    path('spend/', views.SpendView.as_view(), name='spend-list'),
]
