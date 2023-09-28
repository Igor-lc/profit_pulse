from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import RevenueStatistic


class RevenueView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        name = request.query_params.get('name')

        filters = {}
        if date:
            filters['date'] = date
        if name:
            filters['name'] = name

        data = RevenueStatistic.objects.filter(**filters).values('date', 'name').annotate(
            total_revenue=Sum('revenue'),
            total_spend=Sum('spend__spend'),
            total_impressions=Sum('spend__impressions'),
            total_clicks=Sum('spend__clicks'),
            total_conversion=Sum('spend__conversion')
        )

        return Response(data)
