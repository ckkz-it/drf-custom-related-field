from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class WorkingBuilding(models.Model):
    address = models.CharField(max_length=255)


class Employee(models.Model):
    username = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    workplace = models.ForeignKey(WorkingBuilding, null=True, on_delete=models.CASCADE)
