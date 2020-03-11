from django.test import TestCase

from rest_framework.exceptions import ValidationError

from .models import Company, Employee
from .serializers import EmployeeSerializer, EmployeeSerializerWithoutFieldNameSpecified


class CustomRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(name='Great Inc.', country='US')
        self.employee = Employee.objects.create(username='ckkz', company=self.company)

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
