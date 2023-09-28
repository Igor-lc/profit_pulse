from django.urls import path
from . import views

urlpatterns = [
    path('revenue/', views.RevenueView.as_view(), name='revenue-list'),
]
