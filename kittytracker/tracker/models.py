from django.db import models
from django.contrib.postgres.fields import JSONField
import requests, json, datetime
from django.core.files.base import ContentFile
from requests.exceptions import ConnectionError
from django.utils.text import slugify
import itertools

__admin__ = ['Cat', 'Feeding', 'Medication', 'MedicalRecord']

class Weight:
    MEASURE_CHOICES = (
        ('ML', '(ml) Milliliters'),
        ('CC', '(cc) Cubic Centimeters'),
        ('OZ', '(oz) Ounces'),
        ('LB', '(lb) Pounds'),
        ('G', '(G) Grams')
    )
    MILLILITERS = 'ML'
    CUBIC_CENTIMETERS = 'CC'
    OUNCES = 'OZ'
    POUNDS = 'LB'
    GRAMS = 'G'


class Cat(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    MALE = 'M'
    FEMALE = 'F'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    reference_id = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.SlugField(max_length=255, blank=True, null=True,
                                  help_text="This name is auto generated from the name and reference ID. "
                                            "It is used to make it easy to find the animal in a URL lookup.")

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    color = models.CharField(max_length=255, blank=True, null=True)
    weight_unit = models.CharField(max_length=2, choices=Weight.MEASURE_CHOICES, default=Weight.GRAMS)
    weight = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    photo = models.FileField(upload_to="kitty_photos", blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    alert_feeder = models.BooleanField(default=False,
                                       help_text='Alert feeder to critical situations')
    critical_notes = models.TextField(blank=True, null=True)

    first_weight_loss = models.BooleanField(default=False)
    second_weight_loss = models.BooleanField(default=False)
    third_weight_loss = models.BooleanField(default=False)
    many_weight_losses = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # Check to see if slug exists, if it does, make a counter
        self.slug = orig = slugify(self.name)

        for x in itertools.count(1):
            if not Cat.objects.filter(slug=self.slug).exists():
                break
            self.slug = '%s-%d' % (orig, x)

        self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()
        self.short_name = slugify("{name}-{reference_id}".format(name=self.name, reference_id=self.reference_id))

        super(Cat, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'tracker:cat', (self.slug,)

    def __str__(self):
        return self.name


class Feeding(models.Model):
    FOOD_TYPE_CHOICES = (
        ('NA', 'None / Not Entered'),
        ('BO', 'Bottle'),
        ('BS', 'Bottle / Syringe'),
        ('SG', 'Syringe Gruel'),
        ('GG', 'Syringe Gruel / Gruel'),
        ('G',  'Gruel')
    )
    NOT_ENTERED = 'NA'
    BOTTLE = 'BO'
    BOTTLE_SYRINGE = 'BS'
    SYRINGE_GRUEL = 'SG'
    SYRINGE_GRUEL_GRUEL = 'GG'
    GRUEL = 'G'

    STIMULATION_CHOICES = (
        ('NA', 'None / Not Entered'),
        ('UR', 'Urine'),
        ('FE', 'Feces'),
        ('UF', 'Urine / Feces'),
    )
    URINE = 'UR'
    FECES = 'FE'
    URINE_FECES = 'UF'

    cat = models.ForeignKey(Cat, blank=True, null=True)

    weight_unit_measure = models.CharField(max_length=2, choices=Weight.MEASURE_CHOICES, default=Weight.GRAMS)
    weight_before_food = models.IntegerField(blank=True, null=True)
    food_unit_measure = models.CharField(max_length=2, choices=Weight.MEASURE_CHOICES, default=Weight.GRAMS)
    amount_of_food_taken = models.IntegerField(blank=True, null=True)
    food_type = models.CharField(max_length=2, choices=FOOD_TYPE_CHOICES, default=NOT_ENTERED)
    weight_after_food = models.IntegerField(blank=True, null=True)

    stimulated = models.BooleanField(default=False)
    stimulation_type = models.CharField(max_length=2, choices=STIMULATION_CHOICES, default=NOT_ENTERED)

    notes = models.CharField(max_length=2048, blank=True, null=True)

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    photo = models.FileField(upload_to="kitty_photos", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Update Cat's weight if 'Weight After Food' is updated
        if self.weight_after_food:
            self.cat.weight = self.weight_after_food
            self.cat.save()

            # Get all previous cat feedings
            feedings = Feeding.objects.filter(cat=self.cat).order_by('-id')
            if feedings:
                # if the list of cat feedings contains the current, get rid of current from the list
                if feedings[0] == self:
                    feedings = feedings[1:]

                # If the feeding is a weight loss log it as the first/second/third
                if self.weight_after_food < feedings[0].weight_after_food:
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

        # Save time Feeding object modified and created times
        self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        super(Feeding, self).save(*args, **kwargs)

    def __str__(self):
        if self.cat:
            cat_name = self.cat.name
        else:
            cat_name = "NO CAT NAME"
        return "{cat}: {timestamp}".format(cat=self.cat.name, timestamp=self.created)


class Medication(models.Model):
    cat = models.ForeignKey(Cat, blank=True, null=True)

    name = models.CharField(max_length=100)
    duration = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=2)
    dosage_unit = models.CharField(max_length=2, default=Weight.MILLILITERS)
    dosage = models.IntegerField(blank=True, null=True)

    notes = models.CharField(max_length=2048, blank=True, null=True)

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Save time Medication object modified and created times
        self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        super(Medication, self).save(*args, **kwargs)

    def __str__(self):
        if self.cat:
            cat_name = self.cat.name
        else:
            cat_name = "NO CAT NAME"
        return "{cat}: {timestamp}".format(cat=self.cat.name, timestamp=self.created)


class MedicalRecord(models.Model):
    cat = models.ForeignKey(Cat, blank=True, null=True)

    care_given = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    vet_practice = models.CharField(max_length=100)
    doc_name = models.CharField(max_length=100)
    follow_up_date = models.DateField(blank=True, null=True)

    notes = models.CharField(max_length=2048, blank=True, null=True)

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Save time Medication object modified and created times
        self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        super(MedicalRecord, self).save(*args, **kwargs)

    def __str__(self):
        if self.cat:
            cat_name = self.cat.name
        else:
            cat_name = "NO CAT NAME"
        return "{cat}: {timestamp}".format(cat=self.cat.name, timestamp=self.created)
