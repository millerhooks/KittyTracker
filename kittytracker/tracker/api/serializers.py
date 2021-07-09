from kittytracker.tracker.models import Medication, Litter, Cat, CareLog, FosterAlert, VetVisit
from kittytracker.users.models import User
from rest_framework import serializers
from graphene_django.rest_framework.mutation import SerializerMutation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
          'name',
          'user_detail',
        )


class CatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cat
        depth = 1
        fields = (
            'name',
            'slug',
            'foster_manager',
            'litter',
            'gender',
            'cat_type',
            'color',
            'weight_unit',
            'weight',
            'birthday',
            'photo',
            'first_weight_loss',
            'second_weight_loss',
            'third_weight_loss',
            'many_weight_losses',
            'adoption_date',
            'adopted',
            'notes',
            'created',
            'modified',
        )


class MedicationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Medication
        depth = 1
        fields = (
            'name',
            'slug',
            'manufacturer',
            'duration',
            'frequency',
            'dosage_unit',
            'dosage_guidelines',
            'notes',
            'created',
            'modified',
            'package_photo_1',
            'package_photo_2',
            'package_photo_3',
        )


class LitterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Litter
        fields = (
            'name',
            'slug',
            'foster_manager',
            'notes',
            'created',
            'modified',
        )
        extra_kwargs = {
          'foster_manager': {
            'read_only': True,
            'required': False,
            'lookup_field': 'id',
          }
        }


class CareLogSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()
    medication = MedicationSerializer()
    # cat = CatSerializer(read_only=True) this allows put BUT TURNS OFF POST

    class Meta:
        model = CareLog
        fields = (
            'cat',
            'slug',
            'foster_manager',
            'weight_unit_measure',
            'weight_before_food',
            'food_unit_measure',
            'amount_of_food_taken',
            'food_type',
            'weight_after_food',
            'stimulated',
            'medication',
            'medication_dosage_given',
            'medication_dosage_unit',
            'notes',
            'created',
            'photo',
        )
        extra_kwargs = {
            'foster_manager': {
                'read_only': True,
                'required': False,
                'lookup_field': 'id',
            },
            'medication': {
                'read_only': True,
                'required': False,
                'lookup_field': 'slug',
            },
            'cat': {
              'read_only': True,
              'required': False,
              'lookup_field': 'slug',
            },
        }

    @staticmethod
    def create(validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        med_data = validated_data.pop('medication')
        med_obj = Medication.objects.create(**med_data)
        return CareLog.objects.create(cat=cat_obj, medication=med_obj, **validated_data)

    @staticmethod
    def update(instance, validated_data):
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


class FosterAlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FosterAlert
        fields = (
            'subject',
            'slug',
            'created_by',
            'severity',
            'contact_info',
            'cat',
            'description',
            'received_by',
            'received_on',
            'created',
            'modified',
        )
        extra_kwargs = {
          'cat': {
            'read_only': True,
            'required': False,
            'lookup_field': 'slug',
          },
          'created_by': {
            'read_only': True,
            'required': False,
            'lookup_field': 'id',
          },
          'received_by': {
            'read_only': True,
            'required': False,
            'lookup_field': 'id',
          },
        }


class VetVisitSerializer(serializers.HyperlinkedModelSerializer):
    cat = CatSerializer()

    class Meta:
        model = VetVisit
        fields = (
            'cat',
            'slug',
            'foster_manager',
            'care_summary',
            'care_details',
            'appointment',
            'follow_up_date',
            'practice_name',
            'doctor_name',
            'doctor_contact',
            'photo',
            'created',
        )
        extra_kwargs = {
          'cat': {
            'read_only': True,
            'required': False,
            'lookup_field': 'slug',
          },
          'foster_manager': {
            'read_only': True,
            'required': False,
            'lookup_field': 'id',
          }
        }

    @staticmethod
    def create(validated_data):
        cat_data = validated_data.pop('cat')
        cat_obj = Cat.objects.get(**cat_data)
        return VetVisit.objects.create(cat=cat_obj, **validated_data)

