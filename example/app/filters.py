from app.models import TestModel
from django_filters import CharFilter, FilterSet


class MyFilterSet(FilterSet):
    f_field__name = CharFilter()
    f_field__name__istartswith = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = TestModel
        fields = {
            "int_field": ["exact", "isnull"],
            "char_field": ["exact", "isnull"],
            "date_field": ["exact", "isnull"],
            "datetime_field": ["exact", "isnull"],
            "f_field": ["exact", "isnull"],
        }
