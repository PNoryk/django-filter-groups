from django.urls import path
from django_filters.views import FilterView
from django_filters.filterset import FilterSet

from test.models import TestModel


class MyFilterSet(FilterSet):
    class Meta:
        model = TestModel
        fields = {
            'i': ['exact', "isnull"],
            'c': ['exact', "isnull"],
            'd': ['exact', "isnull"],
            'dt': ['exact', "isnull"],
        }


urlpatterns = [
    path("", FilterView.as_view(filterset_class=MyFilterSet, template_name="index.html"))
]