from kittytracker.tracker.models import Medication, Litter, Cat, CareLog, FosterAlert, VetVisit
from kittytracker.users.models import User
from rest_framework import viewsets
from .serializers import MedicationSerializer, LitterSerializer, CatSerializer, \
    CareLogSerializer, FosterAlertSerializer, VetVisitSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('name',)
    lookup_field = 'slug'


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_fields = ('slug', 'name',)
    lookup_field = 'slug'


class LitterViewSet(viewsets.ModelViewSet):
    queryset = Litter.objects.all()
    serializer_class = LitterSerializer
    lookup_field = 'slug'


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_fields = ('slug', 'name',)
    lookup_field = 'slug'


class CareLogViewSet(viewsets.ModelViewSet):
    queryset = CareLog.objects.all()
    serializer_class = CareLogSerializer
    filter_fields = ('cat__slug', 'cat__name', 'food_type')
    lookup_field = 'slug'


class FosterAlertViewSet(viewsets.ModelViewSet):
    queryset = FosterAlert.objects.all()
    serializer_class = FosterAlertSerializer
    filter_fields = ('cat__slug', 'cat__name')
    lookup_field = 'slug'


class VetVisitViewSet(viewsets.ModelViewSet):
    queryset = VetVisit.objects.all()
    serializer_class = VetVisitSerializer
    filter_fields = ('cat__slug', 'cat__name',)
    lookup_field = 'slug'
