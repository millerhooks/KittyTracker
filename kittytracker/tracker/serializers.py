from .models import Cat, Feeding, Medication, MedicalRecord
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class CatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'slug',
            'reference_id',
            'short_name',
            'gender',
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
            'many_weight_losses'
        )


class FeedingSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()

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
        )

    # def create(self, validated_data):
    #     cat_data = validated_data.pop('cat')
    #     feeding = Feeding.objects.create(**validated_data)
    #     Cat.objects.create(feeding=feeding, **cat_data)
    #     return feeding


    def create(self, validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        feeding = Feeding.objects.create(cat=cat_obj, **validated_data)
        return feeding




class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()

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
        )

    def create(self, validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        medicalrecord = MedicalRecord.objects.create(cat=cat_obj, **validated_data)
        return medicalrecord

