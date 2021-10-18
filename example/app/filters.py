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
    custom_filter1 = get_filter_class_with_group_label(django_filters.NumberFilter, "hello1111")(label="1123")

    class Meta:
        model = TestModel
        fields = {
            "int_field": ["exact", "isnull"],
            "char_field": ["exact", "isnull"],
            "date_field": ["exact", "isnull"],
            "datetime_field": ["exact", "isnull"],
            "f_field": ["exact", "isnull"],
        }
