from app.filters import MyFilterSet
from django_filters.views import FilterView


class ExampleView(FilterView):
    filterset_class = MyFilterSet
    template_name = "index.html"
