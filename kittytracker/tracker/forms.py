from django import forms
from .models import Cat
from .widgets import DateTimePicker


class CatForm(forms.ModelForm):

    class Meta:
        model = Cat
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'datetimepicker'})
        }
        fields = ['name',
                  'slug',
                  'foster_manager',
                  'litter',
                  'gender',
                  'cat_type',
                  'color',
                  'weight_unit',
                  'weight',
                  'birthday',
                  'adoption_date',
                  'adopted']
