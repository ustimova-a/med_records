from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()


class Physician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    comment = models.TextField()


class Condition(models.Model):
    name = models.CharField(max_length=50)


class Drug(models.Model):
    name = models.CharField(max_length=50)


class Document(models.Model):
    date_issued = models.DateField()
    physician = models.ForeignKey(Physician, on_delete=models.PROTECT)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)
    prescribed_drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    # source_doc = models.FileField(upload_to=)
    # def user_directory_path(instance, filename):
    # # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'user_{0}/{1}'.format(instance.user.id, filename)
    # + MEDIA_ROOT in settings.py

    