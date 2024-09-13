from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
import csv
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import *
from .serializers import *

def index(request):
    return render(request, 'cars/index.html')

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]



def export_data(request):
    format = request.GET.get('format', 'xlsx')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Country', 'Manufacturer', 'Car', 'Comment'])
        for country in Country.objects.all():
            for manufacturer in country.manufacturers.all():
                for car in manufacturer.cars.all():
                    for comment in car.comments.all():
                        writer.writerow([country.name, manufacturer.name, car.name, comment.comment])
        return response

    wb = Workbook()
    ws = wb.active
    ws.append(['Country', 'Manufacturer', 'Car', 'Comment'])
    for country in Country.objects.all():
        for manufacturer in country.manufacturers.all():
            for car in manufacturer.cars.all():
                for comment in car.comments.all():
                    ws.append([country.name, manufacturer.name, car.name, comment.comment])
    wb.save(response)
    return response