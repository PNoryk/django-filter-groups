from app.models import TestModel
from django_filters import FilterSet


class MyFilterSet(FilterSet):
    class Meta:
        model = TestModel
        fields = {
            "int_field": ["exact", "isnull"],
            "char_field": ["exact", "isnull"],
            "date_field": ["exact", "isnull"],
            "datetime_field": ["exact", "isnull"],
            "f_field": ["exact", "isnull"],
        }
