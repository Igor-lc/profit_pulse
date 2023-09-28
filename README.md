# profit_pulse
Завдання:
Написати файл views.py в revenue. Реалізувати ендпоинт в якому ми отримуємо queryset моделі RevenueStatistic з поділом по дням (date) та назвою (name), з агрегованими сумами значень revenue та пов'язаними значеннями spend, impressions, clicks, conversion з моделі SpendStatistic.
Написати файл views.py в spend. Реалізувати ендпоинт в якому ми отримуємо queryset моделі SpendStatistic з поділом по дням (date) та назвою (name), з агрегованими сумами значень spend, impressions, clicks, conversion та пов'язаними значеннями revenue з моделі RevenueStatistic.
Використовувати засоби Django Rest Framework.
Не створювати серіалайзер.

1. Install Postgresql
2. create database ProfitPulseDB;
3. py -3.11 -m venv virtualenv\profit_pulse
4. pip install psycopg2 django djangorestframework
5. django-admin startproject profit_pulse
6. pip freeze > requirements.txt
8. python manage.py startapp spend
9. python manage.py startapp revenue
10. models.py in Spend:
class SpendStatistic(models.Model):
   name = models.CharField(max_length=255)
   date = models.DateField()
   spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   impressions = models.IntegerField(default=0)
   clicks = models.IntegerField(default=0)
   conversion = models.IntegerField(default=0)

11. models.py in Revenue:
class RevenueStatistic(models.Model):
   name = models.CharField(max_length=255)
   spend = models.ForeignKey('spend.SpendStatistic', on_delete=models.SET_NULL, null=True)
   date = models.DateField()
   revenue = models.DecimalField(max_digits=9, decimal_places=2, default=0)

12. Setting up Postgres, REST API using Django Rest Framework (DRF), creating the appropriate endpoints:
DATABASES = {    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'profitpulsedb',
        'USER': 'postgres',
        'PASSWORD': 'Admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'spend',
    'revenue',
]

13. python manage.py makemigrations
      python manage.py migrate
14. python manage.py createsuperuser
15. Registration in admin.py
from django.contrib import admin
from .models import RevenueStatistic

admin.site.register(RevenueStatistic)

16. revenue\views.py:
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

17. spend\views.py
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

18. revenue\urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('revenue/', views.RevenueView.as_view(), name='revenue-list'),
]

19. spend\urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('spend/', views.SpendView.as_view(), name='spend-list'),
]

20. profit_pulse\urls.py:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('spend.urls')),
    path('api/', include('revenue.urls')),
]

21. create objects:
python manage.py shell
﻿
from revenue.models import RevenueStatistic
from spend.models import SpendStatistic
from datetime import date
﻿
revenue = RevenueStatistic(name="Product A", date=date(2023, 9, 1), revenue=100.50)
revenue.save()

spend = SpendStatistic(name="Product A", date=date(2023, 9, 1), spend=50.25, impressions=1000, clicks=50, conversion=5)
spend.save()

exit()


22. http://localhost:8000/api/spend/
http://localhost:8000/api/revenue/
