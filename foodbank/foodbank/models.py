from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=31)

class Food(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    time = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(Category)

class Donor(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Beneficiary(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Request(models.Model):
    beneficiary = models.ForeignKey(Beneficiary)
    category = models.ForeignKey(Category)
    quantity = models.IntegerField()
    time = models.DateField(default=datetime.date.today)

class Fulfillment(models.Model):
    request = models.ForeignKey(Request)
    quantity = models.IntegerField()
