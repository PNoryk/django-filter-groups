from django import forms, template
from django.utils.translation import gettext_lazy as _

from django_filter_groups.forms import SelectFilterForm

register = template.Library()


def _get_current_filters(filter_set, field_name, lookups):
    current_filters = {}
    for lookup in lookups:
        filter_name = filter_set.get_filter_name(field_name, lookup)
        current_filters[filter_name] = filter_set.filters[filter_name]

    return current_filters


@register.inclusion_tag("filters.html", takes_context=True)
def filters_by_groups(context, filterset_name="filter", request_method="GET"):
    filter_set = context.get(filterset_name)
    filters_data = getattr(context["request"], request_method, {}) or {}
    selected_fields_names = []
    if filters_data:
        selected_fields_names = [
            filter_set.get_filter_name(k.removeprefix("lookup_choice-"), v)
            for k, v in filters_data.items()
            if k.startswith("lookup_choice-")
        ]
    groups_with_filters = {}
    for field_name, lookups in filter_set.get_fields().items():
        current_filters = _get_current_filters(filter_set, field_name, lookups)

        is_field_selected = field_name in selected_fields_names
        groups_with_filters[field_name] = {
            "verbose_name": list(current_filters.values())[0].label,
            "lookups_choice_form": type(
                f"{field_name.capitalize()}LookupsForm",
                (forms.Form,),
                {
                    "prefix": "lookup_choice",
                    _(field_name): forms.ChoiceField(
                        choices=[
                            *(
                                [["", "--------"]]
                                + [[field.lookup_expr, _(field.lookup_expr)] for field in current_filters.values()]
                            )
                        ]
                    ),
                },
            )(filters_data if is_field_selected else None),
            "is_single": len(current_filters) == 1,
            "is_any_selected": any(filter_name in filters_data for filter_name in current_filters),
            "filters_forms": [
                {
                    "form": type(
                        "".join([*map(str.title, name.split("__")), "FiltersForm"]),
                        (forms.Form,),
                        {name: filter_.field},
                    )(filters_data if (is_filter_selected := name in filters_data) else None),
                    "is_filter_selected": is_filter_selected,
                }
                for name, filter_ in current_filters.items()
            ],
        }
    selected_groups_with_filters = {k: v for k, v in groups_with_filters.items() if v["is_any_selected"]}
    select_filter_form = SelectFilterForm(groups_with_filters, filters_data or None)
    context["select_filter_form"] = select_filter_form
    return {
        "groups": groups_with_filters,
        "selected_groups": selected_groups_with_filters,
        "select_filter_form": select_filter_form,
        "filters_request_method": request_method,
    }
