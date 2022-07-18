from app.filters import MyFilterSet
from app.models import TestModel
from django_filters.views import FilterView


class ExampleView(FilterView):
    model = TestModel
    filterset_class = MyFilterSet
    template_name = "index.html"
