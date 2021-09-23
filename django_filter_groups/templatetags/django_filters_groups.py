from django import forms, template
from django.utils.translation import gettext_lazy as _

from django_filter_groups.forms import SelectFilterForm

register = template.Library()


@register.inclusion_tag("filters.html", takes_context=True)
def filters_by_groups(context, filterset_name="filter"):
    filter_set = context.get(filterset_name)
    groups_with_filters = {}
    for field_name, lookups in filter_set.get_fields().items():
        current_filters = {}
        for lookup in lookups:
            filter_name = filter_set.get_filter_name(field_name, lookup)
            current_filters[filter_name] = filter_set.filters[filter_name]
        groups_with_filters[field_name] = {"filters": list(current_filters.values())}
        groups_with_filters[field_name].update(
            {
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
                ),
                "filters_form": type(
                    f"{field_name.capitalize()}FiltersForm",
                    (forms.Form,),
                    {name: filter_.field for name, filter_ in current_filters.items()},
                ),
            }
        )

    return {
        "groups": groups_with_filters,
        "select_filter_form": SelectFilterForm(groups_with_filters),
    }
