# django filter groups

This package groups filters generated by django-filter
The main reason to use it - don't show all filters (show only selected filters)

## how to use
```
pip install django-filter-groups
```
add to your `INSTALLED_APPS` after `django-filter`
```python
INSTALLED_APPS = [
  ...
  "django_filters",
  "django_filters_groups",
  ...
]
```

use it in your template `{% filters_by_groups %}` \
add `{{ select_filter_form.media }}` after adding template tag

If FilterSet name is not 'filter' -> add filterset \
`{% filters_by_groups my_custom_filterset %}`
or filterset name
`{% filters_by_groups "my_custom_filterset" %}`