# cookbook/ingredients/schema.py
import graphene

from graphene_django.types import DjangoObjectType

from .models import Medication, Litter, Cat, CareLog, FosterAlert, VetVisit, User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class MedicationType(DjangoObjectType):
    class Meta:
        model = Medication


class LitterType(DjangoObjectType):
    class Meta:
        model = Litter


class CatType(DjangoObjectType):
    class Meta:
        model = Cat


class CareLogType(DjangoObjectType):
    class Meta:
        model = CareLog


class FosterAlertType(DjangoObjectType):
    class Meta:
        model = FosterAlert


class VetVisitType(DjangoObjectType):
    class Meta:
        model = VetVisit


class Query(object):
    all_users = graphene.List(UserType)
    all_medications = graphene.List(MedicationType)
    all_litters = graphene.List(LitterType)
    all_cats = graphene.List(CatType)
    all_carelogs = graphene.List(CareLogType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_medications(self, info, **kwargs):
        return Medication.objects.all()

    def resolve_all_litters(self, info, **kwargs):
        return Litter.objects.all()

    def resolve_all_cats(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Cat.objects.select_related('litter').all()

    def resolve_all_carelogs(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return CareLog.objects.select_related('cat').all()
