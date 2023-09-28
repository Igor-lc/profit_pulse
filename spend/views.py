from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import SpendStatistic


class SpendView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        name = request.query_params.get('name')

        filters = {}
        if date:
            filters['date'] = date
        if name:
            filters['name'] = name

        data = SpendStatistic.objects.filter(**filters).values('date', 'name').annotate(
            total_spend=Sum('spend'),
            total_impressions=Sum('impressions'),
            total_clicks=Sum('clicks'),
            total_conversion=Sum('conversion'),
            total_revenue=Sum('conversion')
        )

        return Response(data)
