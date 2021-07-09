from django.contrib import admin
from . import models


class LitterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'created', 'modified']


class MedicationAdmin(admin.ModelAdmin):
    search_fields = ['cat__name', 'notes']
    list_display = ['duration', 'notes', 'frequency', 'dosage_guidelines', 'dosage_unit',
                    'created', 'modified']


class CareLogInline(admin.TabularInline):
    model = models.CareLog
    extra = 1
    readonly_fields = ['created']


class CareLogAdmin(admin.ModelAdmin):
    search_fields = ['cat__name', 'amount_of_food_taken', 'notes']
    list_display = ['cat', 'weight_unit_measure', 'weight_before_food', 'food_unit_measure', 'amount_of_food_taken',
                    'food_type', 'weight_after_food', 'stimulated', 'stimulation_type', 'notes', 'photo',
                    'created']


class CatAdmin(admin.ModelAdmin):
    search_fields = ['name', 'reference_id', 'short_name', 'gender', 'notes']
    list_display = ['name', 'slug', 'gender', 'weight', 'weight_unit',
                    'birthday', 'first_weight_loss', 'second_weight_loss',
                    'third_weight_loss', 'many_weight_losses', 'created', 'modified']
    inlines = [
        CareLogInline
    ]


__custom_admins__ = {
    'Cat': CatAdmin,
    'CareLog': CareLogAdmin,
    'Medication': MedicationAdmin,
    'Litter': LitterAdmin,
}

for model in models.__admin__:
    params = [getattr(models, model)]
    if model in __custom_admins__:
        params.append(__custom_admins__[model])
    else:
        _dyn_class = type('%sAdmin' % ( model,), (admin.ModelAdmin,), {})
        params.append(_dyn_class)
    admin.site.register(*params)

admin.site.site_title = 'KittyTracker Admin'
admin.site.site_header = 'KittyTracker Admin'


