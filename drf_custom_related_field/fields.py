from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import is_simple_callable


class CustomRelatedField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Object with {field_name} "{value}" does not exist.'),
        'multiple_objects': _('Multiple objects returned for {field_name} with value "{value}"'),
    }

    def __init__(self, **kwargs):
        custom_field_name = kwargs.pop('field_name', None)
        super().__init__(**kwargs)

        assert custom_field_name is not None, '`field_name` option should be provided'

        if is_simple_callable(custom_field_name):
            custom_field_name = custom_field_name()
        assert isinstance(custom_field_name, str), \
            '`field_name` have to be `str` type or callable with no arguments that return `str`'

        self.custom_field_name = custom_field_name

    def to_representation(self, model: Model):
        value = getattr(model, self.custom_field_name)
        if is_simple_callable(value):
            return value()
        return value

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.custom_field_name: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', value=data, field_name=self.custom_field_name)
        except MultipleObjectsReturned:
            self.fail('multiple_objects', value=data, field_name=self.custom_field_name)
