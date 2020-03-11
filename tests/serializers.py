from rest_framework import serializers

from drf_custom_related_field import CustomRelatedField

from .models import Company, Employee, WorkingBuilding


class EmployeeSerializer(serializers.ModelSerializer):
    company = CustomRelatedField(queryset=Company.objects, field_name='name')

    class Meta:
        model = Employee
        fields = ('username', 'company')


def get_field_name():
    return 'name'


class EmployeeWithCallableFieldNameSerializer(serializers.ModelSerializer):
    company = CustomRelatedField(field_name=get_field_name, read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'company')


class EmployeeWithCallableForeignKeyFieldSerializer(serializers.ModelSerializer):
    company = CustomRelatedField(field_name='upper_name', read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'company')


class EmployeeWithNestedSourceFieldSerializer(serializers.ModelSerializer):
    workplace = CustomRelatedField(source='workplace.address', field_name='street', read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'workplace')


class EmployeeWithNestedSourceFieldCallableSerializer(serializers.ModelSerializer):
    workplace = CustomRelatedField(source='workplace.address', field_name='full_address', read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'workplace')


class EmployeeWithNestedOneLevelSerializer(serializers.ModelSerializer):
    workplace_capacity = CustomRelatedField(source='workplace', field_name='capacity', read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'workplace_capacity')


class WorkingBuildingSerializer(serializers.ModelSerializer):
    employees = CustomRelatedField(field_name='username', many=True, read_only=True)

    class Meta:
        model = WorkingBuilding
        fields = ('capacity', 'employees')
