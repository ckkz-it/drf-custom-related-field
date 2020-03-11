from rest_framework import serializers

from drf_custom_related_field import CustomRelatedField

from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    company = CustomRelatedField(queryset=Company.objects.all(), field_name='name')

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSerializerWithoutFieldNameSpecified(serializers.ModelSerializer):
    company = CustomRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'
