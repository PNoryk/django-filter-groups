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

use it in your template:
- add `{% add_select_filter_form_to_context %}` to the top of your template. 
  It allows you to place `{{ select_filter_form.media }}` anywhere you want
- add `{% filters_by_groups %}`
- add `{{ select_filter_form.media }}`

If FilterSet name is not 'filter' -> add filterset \
`{% add_select_filter_form_to_context my_custom_filterset %}`\
`{% filters_by_groups my_custom_filterset %}`
or filterset name
`{% filters_by_groups "my_custom_filterset" %}`
`{% add_select_filter_form_to_context "my_custom_filterset" %}`


## default settings

```
# django settings
FILTERS_GROUPS_SELECT_FILTER_FORM_LABEL = "Select a label"
```
```js
// static/django_filters_groups/filter-defaults.js
let filterDefaults = {
  filterWrapperSelector: "p", // p is necessary when you use {{ form.as_p }}
  submitOnFilterDelete: false,
};
```