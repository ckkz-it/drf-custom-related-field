from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def upper_name(self):
        return self.name.upper()


class Address(models.Model):
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)

    def full_address(self):
        return f'{self.street}, {self.building}'


class WorkingBuilding(models.Model):
    capacity = models.IntegerField(default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Employee(models.Model):
    username = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    workplace = models.ForeignKey(WorkingBuilding, null=True, on_delete=models.CASCADE, related_name='employees')
