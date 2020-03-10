from rest_framework import serializers

from drf_custom_related_field import CustomRelatedField

from .models import Employee, Company


class EmployeeSerializer(serializers.ModelSerializer):
    company = CustomRelatedField(queryset=Company.objects.all(), field_name='name')

    class Meta:
        model = Employee
        fields = '__all__'
