from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CustomRelatedField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Object with {field_name} "{value}" does not exist.'),
        # TODO: add type validation
    }

    def __init__(self, **kwargs):
        custom_field_name = kwargs.pop('field_name', None)
        super().__init__(**kwargs)

        assert custom_field_name is not None, '`field_name` option should be provided'
        assert isinstance(custom_field_name, str), '`field_name` have to be `str` type'

        self.custom_field_name = custom_field_name

    def to_representation(self, model: Model):
        return getattr(model, self.custom_field_name)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.custom_field_name: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', value=data, field_name=self.custom_field_name)
