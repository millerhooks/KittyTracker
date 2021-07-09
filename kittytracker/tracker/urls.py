from django.conf.urls import url
from .views import MedicationList, MedicationCreate, MedicationDelete, MedicationUpdate, \
    LitterList, LitterCreate, LitterDelete, LitterUpdate, \
    CatList, CatCreate, CatDelete, CatUpdate, \
    CareLogList, CareLogCreate, CareLogDelete, CareLogUpdate

urlpatterns = [
    url('carelog/list/', CareLogList.as_view(), name='carelog-list'),
    url('carelog/add/', CareLogCreate.as_view(), name='carelog-add'),
    url('carelog/<slug:slug>/', CareLogUpdate.as_view(), name='carelog-update'),
    url('carelog/<slug:slug>/delete/', CareLogDelete.as_view(), name='carelog-delete'),

    url('cat/list/', CatList.as_view(), name='cat-list'),
    url('cat/add/', CatCreate.as_view(), name='cat-add'),
    url('cat/<slug:slug>/', CatUpdate.as_view(), name='cat-update'),
    url('cat/<slug:slug>/delete/', CatDelete.as_view(), name='cat-delete'),

    url('litter/list/', LitterList.as_view(), name='litter-list'),
    url('litter/add/', LitterCreate.as_view(), name='litter-add'),
    url('litter/<slug:slug>/', LitterUpdate.as_view(), name='litter-update'),
    url('litter/<slug:slug>/delete/', LitterDelete.as_view(), name='litter-delete'),

    url('meds/list/', MedicationList.as_view(), name='meds-list'),
    url('meds/add/', MedicationCreate.as_view(), name='meds-add'),
    url('meds/<slug:slug>/', MedicationUpdate.as_view(), name='meds-update'),
    url('meds/<slug:slug>/delete/', MedicationDelete.as_view(), name='meds-delete'),
]
# What IS THIS FILE ?
