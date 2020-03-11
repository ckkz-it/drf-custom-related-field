from django.test import TestCase

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from drf_custom_related_field import CustomRelatedField

from .models import Address, Company, Employee, WorkingBuilding
from .serializers import (
    EmployeeSerializer,
    EmployeeWithCallableFieldNameSerializer,
    EmployeeWithCallableForeignKeyFieldSerializer,
    EmployeeWithNestedOneLevelSerializer,
    EmployeeWithNestedSourceFieldCallableSerializer,
    EmployeeWithNestedSourceFieldSerializer,
    WorkingBuildingSerializer,
)


class CustomRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.work_address = Address.objects.create(street='Main st.', building='10')
        self.workplace = WorkingBuilding.objects.create(capacity=200, address=self.work_address)
        self.company = Company.objects.create(name='Great Inc.', country='US', )
        self.employee = Employee.objects.create(username='ckkz', company=self.company, workplace=self.workplace)

    def test_getting_foreign_key(self):
        serializer = EmployeeSerializer(self.employee)
        data = serializer.data
        self.assertIn('company', data)
        self.assertEqual(data['company'], self.company.name)

    def test_assign_value_to_model(self):
        new_company = Company.objects.create(name='New Company', country='RU')
        serializer = EmployeeSerializer(self.employee, data={'company': new_company.name}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.company_id, new_company.id)

    def test_assign_not_existing_object(self):
        serializer = EmployeeSerializer(self.employee, data={'company': 'Non existing name'}, partial=True)
        with self.assertRaises(ValidationError) as error_ctx:
            serializer.is_valid(raise_exception=True)
        exc = error_ctx.exception
        self.assertEqual(exc.status_code, 400)
        self.assertIn('company', exc.detail)
        self.assertEqual(exc.detail['company'][0].code, 'does_not_exist')

    def test_without_field_name_specified(self):
        with self.assertRaises(AssertionError) as error_ctx:
            class _(serializers.ModelSerializer):
                company = CustomRelatedField(queryset=Company.objects.all())

                class Meta:
                    model = Employee
                    fields = ('username', 'company')

        self.assertTrue('should be provided' in str(error_ctx.exception))

    def test_wrong_format_field_name(self):
        with self.assertRaises(AssertionError) as error_ctx:
            class _(serializers.ModelSerializer):
                company = CustomRelatedField(queryset=Company.objects.all(), field_name=132)

                class Meta:
                    model = Employee
                    fields = ('username', 'company')

        self.assertTrue('have to be `str` type or callable' in str(error_ctx.exception))

    def test_callable_field_name(self):
        serializer = EmployeeWithCallableFieldNameSerializer(self.employee)
        self.assertEqual(serializer.data['company'], self.employee.company.name)

    def test_wrong_callable_field_name(self):
        def get_field_name_wrong(some_arg):
            return some_arg + 'name'

        with self.assertRaises(AssertionError) as error_ctx:
            class _(serializers.ModelSerializer):
                company = CustomRelatedField(field_name=get_field_name_wrong, read_only=True)

                class Meta:
                    model = Employee
                    fields = ('username', 'company')

        self.assertTrue('have to be `str` type or callable' in str(error_ctx.exception))

    def test_callable_foreign_key_field(self):
        serializer = EmployeeWithCallableForeignKeyFieldSerializer(self.employee)
        self.assertEqual(serializer.data['company'], self.employee.company.upper_name())

    def test_nested_custom_field(self):
        serializer = EmployeeWithNestedSourceFieldSerializer(self.employee)
        self.assertEqual(serializer.data['workplace'], self.employee.workplace.address.street)

    def test_nested_callable_custom_field(self):
        serializer = EmployeeWithNestedSourceFieldCallableSerializer(self.employee)
        self.assertEqual(serializer.data['workplace'], self.employee.workplace.address.full_address())

    def test_nested_with_one_level(self):
        serializer = EmployeeWithNestedOneLevelSerializer(self.employee)
        self.assertEqual(serializer.data['workplace_capacity'], self.workplace.capacity)

    def test_many(self):
        serializer = WorkingBuildingSerializer(self.workplace)
        self.assertEqual(len(serializer.data['employees']), self.workplace.employees.count())
        self.assertTrue(Employee.objects.filter(username=serializer.data['employees'][0]).exists())
