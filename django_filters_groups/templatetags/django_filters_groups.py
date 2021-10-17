from collections import defaultdict

from django import forms, template
from django.utils.translation import gettext_lazy as _

from django_filters_groups.forms import SelectFilterForm

register = template.Library()


def _get_current_filters(filter_set, field_name, lookups):
    current_filters = {}
    for lookup in lookups:
        filter_name = filter_set.get_filter_name(field_name, lookup)
        current_filters[filter_name] = filter_set.filters[filter_name]

    return current_filters


@register.inclusion_tag("django_filters_groups/filters.html", takes_context=True)
def filters_by_groups(context, filterset="filter"):
    filter_set = context.get(filterset) if isinstance(filterset, str) else filterset
    filters_data = context["request"].GET
    lookup_form_prefix = "lookup_choice"

    selected_fields = {}
    if filters_data:
        selected_fields = {
            k[len(lookup_form_prefix + "-") :]: v
            for k, v in filters_data.items()
            # leave it to not to override lookup with filter value
            if k.startswith(lookup_form_prefix + "-")
        }

    filters_by_groups_ = defaultdict(lambda: defaultdict(dict))
    for filter_ in filter_set.filters.values():
        group_name = filter_.field_name
        group_ends_with = f"__{filter_.lookup_expr}"
        if group_name.endswith(group_ends_with):
            group_name = group_name[: len(group_ends_with)]
        filters_by_groups_[group_name][filter_.lookup_expr] = filter_
    groups_with_filters = {}
    for field_name, group_dct in filters_by_groups_.items():
        is_field_selected = field_name in selected_fields
        groups_with_filters[field_name] = {
            "verbose_name": list(group_dct.values())[0].label,
            "lookups_choice_form": type(
                f"{field_name.capitalize()}LookupForm",
                (forms.Form,),
                {
                    "prefix": lookup_form_prefix,
                    field_name: forms.ChoiceField(
                        choices=[
                            *(
                                [["", "--------"]]
                                + [[lookup, _(filter_.lookup_expr)] for lookup, filter_ in group_dct.items()]
                            )
                        ]
                    ),
                },
            )(filters_data if is_field_selected else None),
            "filters_forms": [
                {
                    "form": type(
                        "".join(
                            [
                                *map(
                                    str.title,
                                    (
                                        filter_name := "__".join(
                                            filter(bool, [field_name, lookup_name if lookup_name != "exact" else ""])
                                        )
                                    ).split("__"),
                                ),
                                "FiltersForm",
                            ]
                        ),
                        (forms.Form,),
                        {filter_name: filter_.field},
                    )(filters_data if (is_filter_selected := lookup_name == selected_fields.get(field_name)) else None),
                    "is_filter_selected": is_filter_selected,
                }
                for lookup_name, filter_ in group_dct.items()
            ],
        }
    selected_groups_with_filters = {
        lookup: filter_ for lookup, filter_ in groups_with_filters.items() if lookup in selected_fields
    }
    select_filter_form = SelectFilterForm(groups_with_filters, filter_set.form.media, filters_data or None)
    context["select_filter_form"] = select_filter_form
    return {
        "groups": groups_with_filters,
        "selected_groups": selected_groups_with_filters,
        "select_filter_form": select_filter_form,
    }
