from django.db import models
import requests, datetime
from django.urls import reverse
from django_autoslugfield import AutoSlugField
from kittytracker.users.models import User


__admin__ = ['Medication', 'Litter', 'Cat', 'CareLog', 'FosterAlert', 'VetVisit']


class Litter(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)
    foster_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        super(Litter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cat(models.Model):
    MEASURE_CHOICES = (
      ('OZ', '(oz) Ounces'),
      ('LB', '(lb) Pounds'),
      ('G', '(G) Grams')
    )
    OUNCES = 'OZ'
    POUNDS = 'LB'
    GRAMS = 'G'

    GENDER_CHOICES = (
      ('M', 'Male'),
      ('F', 'Female')
    )
    MALE = 'M'
    FEMALE = 'F'

    CAT_TYPE = (
      ('O', 'Orphan'),
      ('P', 'Pregnant'),
      ('NK', 'Nursing Kitten'),
      ('NM', 'Nursing Mom'),
      ('A', 'Adult')
    )
    ORPHAN = 'O'
    PREGNANT = 'P'
    NURSING_KITTEN = 'NK'
    NURSING_MOM = 'NM'
    ADULT = 'A'

    name = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)
    foster_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    litter = models.ForeignKey(Litter, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    cat_type = models.CharField(max_length=1, choices=CAT_TYPE, default=ORPHAN)

    color = models.CharField(max_length=255, blank=True, null=True)
    weight_unit = models.CharField(max_length=2, choices=MEASURE_CHOICES, default=GRAMS)
    weight = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    photo = models.FileField(upload_to="kitty_photos", blank=True, null=True)

    first_weight_loss = models.BooleanField(default=False)
    second_weight_loss = models.BooleanField(default=False)
    third_weight_loss = models.BooleanField(default=False)
    many_weight_losses = models.BooleanField(default=False)

    adoption_date = models.DateField(blank=True, null=True)
    adopted = models.BooleanField(default=False)

    notes = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        super(Cat, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'tracker:cat', (self.slug,)

    @property
    def litter_mates(self):
        return Cat.objects.filter(litter=self.litter)

    def __str__(self):
        return self.name


class Medication(models.Model):
    MEASURE_CHOICES = (
        ('ML', '(ml) Milliliters'),
        ('CC', '(cc) Cubic Centimeters'),
        ('OZ', '(oz) Ounces'),
        ('G', '(G) Grams')
    )
    MILLILITERS = 'ML'
    CUBIC_CENTIMETERS = 'CC'
    OUNCES = 'OZ'
    GRAMS = 'G'

    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=2)
    dosage_unit = models.CharField(max_length=2, choices=MEASURE_CHOICES, blank=True, null=True)
    dosage_guidelines = models.TextField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    package_photo_1 = models.FileField(upload_to="medication_package_photos", blank=True, null=True)
    package_photo_2 = models.FileField(upload_to="medication_package_photos", blank=True, null=True)
    package_photo_3 = models.FileField(upload_to="medication_package_photos", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        super(Medication, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('medication', kwargs={'slug': self.slug})

    def __str__(self):
        return "{medication}: {manufacturer}".format(medication=self.name, manufacturer=self.manufacturer)


class CareLog(models.Model):
    WEIGHT_MEASURE_CHOICES = (
        ('OZ', '(oz) Ounces'),
        ('LB', '(lb) Pounds'),
        ('G', '(G) Grams')
    )
    OUNCES = 'OZ'
    POUNDS = 'LB'
    GRAMS = 'G'

    VOLUME_MEASURE_CHOICES = (
        ('ML', '(ml) Milliliters'),
        ('CC', '(cc) Cubic Centimeters'),
        ('OZ', '(oz) Ounces'),
        ('G', '(G) Grams')
    )
    MILLILITERS = 'ML'
    CUBIC_CENTIMETERS = 'CC'

    FOOD_TYPE_CHOICES = (
        ('MN', 'Mom (Nursing)'),
        ('BO', 'Bottle'),
        ('BS', 'Bottle / Syringe'),
        ('SG', 'Syringe Gruel'),
        ('GG', 'Syringe Gruel / Gruel'),
        ('G',  'Gruel')
    )
    BOTTLE = 'BO'
    BOTTLE_SYRINGE = 'BS'
    SYRINGE_GRUEL = 'SG'
    SYRINGE_GRUEL_GRUEL = 'GG'
    GRUEL = 'G'

    STIMULATION_CHOICES = (
        ('UR', 'Urine'),
        ('FE', 'Feces'),
        ('UF', 'Urine / Feces'),
    )
    URINE = 'UR'
    FECES = 'FE'
    URINE_FECES = 'UF'

    cat = models.ForeignKey(Cat)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)

    foster_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    weight_unit_measure = models.CharField(max_length=2, choices=WEIGHT_MEASURE_CHOICES, default=GRAMS)
    weight_before_food = models.IntegerField(blank=True, null=True)
    food_unit_measure = models.CharField(max_length=2, choices=WEIGHT_MEASURE_CHOICES, default=GRAMS)
    amount_of_food_taken = models.IntegerField(blank=True, null=True)
    food_type = models.CharField(max_length=2, choices=FOOD_TYPE_CHOICES, blank=True, null=True)
    weight_after_food = models.IntegerField(blank=True, null=True, default=0)

    stimulated = models.BooleanField(default=False)
    stimulation_type = models.CharField(max_length=2, choices=STIMULATION_CHOICES, blank=True, null=True)

    medication = models.ForeignKey(Medication, blank=True, null=True, on_delete=models.SET_NULL)
    medication_dosage_given = models.FloatField(blank=True, null=True)
    medication_dosage_unit = models.CharField(max_length=2, choices=VOLUME_MEASURE_CHOICES, blank=True, null=True,
                                              help_text="If left blank this will default to "
                                                        "the default unit for the medication.")

    notes = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    photo = models.FileField(upload_to="kitty_photos", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Update Cat's weight if 'Weight After Food' is updated
        if self.weight_after_food:
            self.cat.weight = self.weight_after_food
            self.cat.save()

            # Get all previous cat feedings
            feedings = CareLog.objects.filter(cat=self.cat).order_by('-id')
            if feedings:
                # if the list of cat feedings contains the current, get rid of current from the list
                if feedings[0] == self:
                    feedings = feedings[1:]

                # If the feeding is a weight loss log it as the first/second/third
                if feedings[0].weight_after_food is not None and self.weight_after_food < feedings[0].weight_after_food:
                    if self.cat.first_weight_loss:
                        self.cat.second_weight_loss = True
                    elif self.cat.second_weight_loss:
                        self.cat.third_weight_loss = True
                    elif self.cat.third_weight_loss:
                        self.cat.many_weight_losses = True
                    elif not self.cat.first_weight_loss:
                        self.cat.first_weight_loss = True

                # Save Cat Object
                self.cat.save()

        if self.medication and not self.medication_dosage_unit:
            self.medication_dosage_unit = self.medication.dosage_unit

        super(CareLog, self).save(*args, **kwargs)

    def __str__(self):
        return "{cat}: {timestamp}".format(cat=self.cat.name, timestamp=self.created)


class FosterAlert(models.Model):
    SEVERITY_CHOICES = (
        ('0', 'Notice'),
        ('1', 'Warning'),
        ('2', 'Danger'),
        ('3', 'Critical'),
        ('4', 'Emergency'),
    )
    NOTICE = '0'
    WARNING = '1'
    DANGER = '2'
    CRITICAL = '3'
    EMERGENCY = '4'

    subject = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name="foster_alert_created_by")

    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES, default=NOTICE)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    cat = models.ForeignKey(Cat, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    received_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name="foster_alert_received_by")
    received_on = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{cat} - {subject}: {timestamp}".format(cat=self.cat.name, subject=self.subject, timestamp=self.created)


class VetVisit(models.Model):
    cat = models.ForeignKey(Cat)
    slug = AutoSlugField(max_length=255, unique=True, blank=True, null=True)

    foster_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    care_summary = models.CharField(max_length=255, blank=True, null=True)
    care_details = models.TextField(blank=True, null=True)

    appointment = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateTimeField(blank=True, null=True)

    practice_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_contact = models.CharField(max_length=255, blank=True, null=True)

    photo = models.FileField(upload_to="kitty_photos", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(VetVisit, self).save(*args, **kwargs)

    def __str__(self):
        return "{cat}: {practice} {timestamp}".format(cat=self.cat.name, timestamp=self.appointment,
                                                      practice=self.practice_name)

