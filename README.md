DRF Custom Related Field
========================

This is a Django REST Framework's `PrimaryKeyRelatedField` like field which
allows you to pass custom fields (instead of default pk) to serialize relation.

Requirements
============

- Python 3.6+
- Django 2+
- djangorestframework 3+

Installation
============

```
pip install drf-custom-related-field
```

Usage
=====

For example, we have following model structure:

```python
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
```

And we have following instances:

```python
work_address = Address.objects.create(street='Main st.', building='10')
workplace = WorkingBuilding.objects.create(capacity=200, address=work_address)
company = Company.objects.create(name='Great Inc.', country='US', )
employee = Employee.objects.create(username='ckkz', company=company, workplace=workplace)
```

Examples:

1. Map custom field for read only
    ```python
    class EmployeeSerializer(serializers.ModelSerializer):
       company = CustomRelatedField(queryset=Company.objects, field_name='name')

       class Meta:
           model = Employee
           fields = ('username', 'company')

    serializer = EmployeeSerializer(employee)
    assert serializer.data['company'] == company.name
    ```
      ```json
   {
    "username": "ckkz",
    "company": "Great Inc."
   } 
   ```

2. Assign new value by custom field (`name` in this case)
    ```python
    class EmployeeSerializer(serializers.ModelSerializer):
       company = CustomRelatedField(queryset=Company.objects, field_name='name')

       class Meta:
           model = Employee
           fields = ('username', 'company')
   
    new_company = Company.objects.create(name='New Company', country='RU')
    serializer = EmployeeSerializer(employee, data={'company': new_company.name}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    employee.refresh_from_db()
    assert employee.company_id == new_company.id
    ```   
   ```json
   {
    "username": "ckkz",
    "company": "New Company"
   } 
   ```

3. Use `many=True`
    ```python
    class WorkingBuildingSerializer(serializers.ModelSerializer):
       employees = CustomRelatedField(field_name='username', many=True, read_only=True)

       class Meta:
           model = WorkingBuilding
           fields = ('capacity', 'employees')

    serializer = WorkingBuildingSerializer(workplace)
    assert len(serializer.data['employees']) == workplace.employees.count()
    ```
   ```json
    {
     "capacity": 200,
     "employees": ["ckkz"]
    }
    ```

4. Use nested (dotted) relations and callable model fields
    ```python
    class EmployeeSerializer(serializers.ModelSerializer):
       workplace = CustomRelatedField(source='workplace.address', field_name='full_address', read_only=True)

       class Meta:
           model = Employee
           fields = ('username', 'workplace')

   serializer = EmployeeSerializer(employee)
   assert serializer.data['workplace'] == employee.workplace.address.full_address() 
    ```
   ```json
    {
     "username": "ckkz",
     "workplace": "Main st., 10"
    }
    ```
