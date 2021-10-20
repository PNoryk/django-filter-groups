import django_filters
from app.models import TestModel
from django.db.models import Count

from django_filters_groups.utils import get_filter_class_with_group_label


class FFieldCountFilter(django_filters.NumberFilter):
    filter_group_label = "custom_group_label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = self.filter_method
        self.label = "label"

    @staticmethod
    def filter_method(queryset, _, value):
        return queryset.annotate(c=Count("f_field__f2")).filter(c=value)


class MyFilterSet(django_filters.FilterSet):
    f_field__name = django_filters.CharFilter()
    f_field__name__istartswith = django_filters.CharFilter(lookup_expr="istartswith")

    custom_filter = FFieldCountFilter(label="1")
    custom_filter1 = get_filter_class_with_group_label(django_filters.NumberFilter, "custom group name")(
        label="int_field", method="custom_filter_method"
    )
    custom_filter1__isnull = django_filters.NumberFilter(
        lookup_expr="isnull",
        label="int_field is null",
        method="custom_filter_method",
    )

    @staticmethod
    def custom_filter_method(queryset, name, value):
        queryset.filter(**{f"int_field__{name}": value})

    class Meta:
        model = TestModel
        fields = {
            "char_field": ["exact", "isnull"],
            "date_field": ["exact", "isnull"],
            "datetime_field": ["exact", "isnull"],
            "f_field": ["exact", "isnull"],
        }
