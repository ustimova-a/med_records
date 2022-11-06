from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(default=None)

    def __str__(self):
        return str(self.name)


class Specialty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Specialties'


class Physician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    is_recommended = models.BooleanField(default=False)
    comment = models.TextField()

    def __str__(self):
        return str(self.last_name)


class Condition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Drug(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Document(models.Model):
    date_issued = models.DateField()
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    prescribed_drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    source_doc = models.FileField(upload_to="uploads/%Y/%m/%d/")

    def __str__(self):
        return str(self.id)


class Treatment(models.Model):
    prescribed_drug = models.ManyToManyField(Drug)
    dosage = models.FloatField(validators=[MinValueValidator(0)])
    dosing_regimen = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return str(self.id)


   

    