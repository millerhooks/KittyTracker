from __future__ import unicode_literals
from django.contrib import admin
from jsoneditor.forms import JSONEditor
from django.contrib.postgres.fields import JSONField
from . import models as tracker_models
from import_export.admin import ImportExportModelAdmin

from import_export import resources


class MedicationResource(resources.ModelResource):

    class Meta:
        model = tracker_models.Medication


class FeedingResource(resources.ModelResource):

    class Meta:
        model = tracker_models.Feeding


class CatResource(resources.ModelResource):

    class Meta:
        model = tracker_models.Cat


class MedicationAdmin(ImportExportModelAdmin):
    search_fields = ['cat__name', 'notes']
    list_display = ['cat', 'duration', 'notes', 'frequency', 'dosage', 'dosage_unit',
                    'created', 'modified']
    resource_class = MedicationResource


class FeedingInline(admin.TabularInline):
    model = tracker_models.Feeding
    extra = 1
    exclude = ['modified']
    readonly_fields = ['created']


class FeedingAdmin(ImportExportModelAdmin):
    search_fields = ['cat__name', 'amount_of_food_taken', 'notes']
    list_display = ['cat', 'weight_unit_measure', 'weight_before_food', 'food_unit_measure', 'amount_of_food_taken',
                    'food_type', 'weight_after_food', 'stimulated', 'stimulation_type', 'notes', 'photo',
                    'created', 'modified']
    resource_class = FeedingResource


class CatAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'reference_id', 'short_name', 'gender', 'notes']
    list_display = ['name', 'reference_id', 'short_name', 'gender', 'weight_unit', 'weight', 'notes', 'birthday', 'photo',
                    'alert_feeder', 'critical_notes', 'first_weight_loss', 'second_weight_loss', 'third_weight_loss',
                    'many_weight_losses', 'created', 'modified']
    inlines = [
        FeedingInline
    ]
    resource_class = CatResource


__custom_admins__ = {
    'Cat': CatAdmin,
    'Feeding': FeedingAdmin,
    'Medication': MedicationAdmin,
}

for model in tracker_models.__admin__:
    params = [getattr(tracker_models, model)]
    if model in __custom_admins__:
        params.append(__custom_admins__[model])
    else:
        _dyn_class = type('%sAdmin' % ( model,), (admin.ModelAdmin,), {})
        params.append(_dyn_class)
    admin.site.register(*params)

admin.site.site_title = 'KittyTracker Admin'
admin.site.site_header = 'KittyTracker Admin'
