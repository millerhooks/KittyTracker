from .models import Litter, Cat, Feeding, Medication, MedicalRecord
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class LitterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Litter
        fields = (
            'id',
            'litter_name',
            'mom_cat',
            'showRow'
        )


class CatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cat
        depth = 1
        fields = (
            'id',
            'name',
            'slug',
            'reference_id',
            'short_name',
            'gender',
            'age',
            'cat_type',
            'litter_mates',
            'color',
            'weight_unit',
            'weight',
            'notes',
            'birthday',
            'photo',
            'created',
            'modified',
            'alert_feeder',
            'critical_notes',
            'first_weight_loss',
            'second_weight_loss',
            'third_weight_loss',
            'many_weight_losses',
            'showRow'
        )


class FeedingSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()
    # cat = CatSerializer(read_only=True) this allows put BUT TURNS OFF POST

    class Meta:
        model = Feeding
        fields = (
            'id',
            'cat',
            'weight_unit_measure',
            'weight_before_food',
            'food_unit_measure',
            'amount_of_food_taken',
            'food_type',
            'weight_after_food',
            'stimulated',
            'stimulation_type',
            'notes',
            'created',
            'modified',
            'photo',
            'showRow',
        )
        extra_kwargs = {
            'cat':{
                'read_only': True,
                'required': False
            }
        }

    def create(self, validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        feeding = Feeding.objects.create(cat=cat_obj, **validated_data)
        return feeding

    def update(self, instance, validated_data):
        instance.weight_unit_measure = validated_data['weight_unit_measure']
        instance.weight_before_food = validated_data['weight_before_food']
        instance.food_unit_measure = validated_data['food_unit_measure']
        instance.amount_of_food_taken = validated_data['amount_of_food_taken']
        instance.food_type = validated_data['food_type']
        instance.weight_after_food = validated_data['weight_after_food']
        instance.stimulated = validated_data['stimulated']
        instance.stimulation_type = validated_data['stimulation_type']
        instance.notes = validated_data['notes']
        instance.save()


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()
    # cat = CatSerializer(read_only=True)

    class Meta:
        model = Medication
        fields = (
            'id',
            'cat',
            'name',
            'duration',
            'frequency',
            'dosage_unit',
            'dosage',
            'notes',
            'created',
            'modified',
            'showRow',
        )

    def create(self, validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        medication = Medication.objects.create(cat=cat_obj, **validated_data)
        return medication





class MedicalRecordSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()

    class Meta:
        model = MedicalRecord
        fields = (
            'id',
            'cat',
            'care_given',
            'date',
            'vet_practice',
            'doc_name',
            'follow_up_date',
            'notes',
            'showRow'
        )

    def create(self, validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        medicalrecord = MedicalRecord.objects.create(cat=cat_obj, **validated_data)
        return medicalrecord

