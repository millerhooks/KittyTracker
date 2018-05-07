from .models import Cat, Feeding, Medication, MedicalRecord
from rest_framework import viewsets
from .serializers import CatSerializer, FeedingSerializer, MedicationSerializer, MedicalRecordSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import django_filters


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_fields = ('slug', 'name',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class FeedingViewSet(viewsets.ModelViewSet):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
    filter_fields = ('cat__slug', 'cat__name',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_fields = ('cat__slug', 'cat__name')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filter_fields = ('cat__slug', 'cat__name',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
