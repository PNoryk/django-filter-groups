from collections import defaultdict

from django import forms, template
from django_filters.conf import settings as django_filters_settings
from django_filters.utils import label_for_filter

from django_filters_groups.forms import SelectFilterForm

register = template.Library()

FILTERS_VERBOSE_LOOKUPS = django_filters_settings.VERBOSE_LOOKUPS


def _get_current_filters(filter_set, field_name, lookups):
    current_filters = {}
    for lookup in lookups:
        filter_name = filter_set.get_filter_name(field_name, lookup)
        current_filters[filter_name] = filter_set.filters[filter_name]

    return current_filters


def _filters_by_groups(context, filterset="filter"):
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
            group_name = group_name[: -len(group_ends_with)]
        filters_by_groups_[group_name][filter_.lookup_expr] = filter_
    groups_with_filters = {}
    for field_name, group_dct in filters_by_groups_.items():
        is_field_selected = field_name in selected_fields

        filter_group_label = None
        for filter_ in group_dct.values():
            filter_group_label = getattr(filter_, "filter_group_label", None)
            if filter_group_label:
                break

        filter_ = group_dct.get("exact", list(group_dct.values())[0])
        if not (verbose_name := getattr(filter_, "_verbose_name", None)):
            verbose_name = filter_._label
            if verbose_name is None:
                verbose_name = label_for_filter(filter_set._meta.model, field_name, None)
            verbose_lookup = " " + FILTERS_VERBOSE_LOOKUPS.get(filter_.lookup_expr, filter_.lookup_expr)
            if (verbose_name or "").endswith(verbose_lookup):
                verbose_name = verbose_name[: -len(verbose_lookup)]
        verbose_name = filter_group_label or verbose_name

        # save verbose_name to the filter because this function is called twice.
        # the filter "_label" will has been already changed in the second time.
        # it happens in filter "field" property
        filter_._verbose_name = verbose_name
        groups_with_filters[field_name] = {
            "verbose_name": verbose_name,
            "lookups_choice_form": type(
                f"{field_name.capitalize()}LookupForm",
                (forms.Form,),
                {
                    "prefix": lookup_form_prefix,
                    field_name: forms.ChoiceField(
                        label=verbose_name,
                        choices=[
                            *(
                                [["", "--------"]]
                                + [
                                    [
                                        lookup,
                                        FILTERS_VERBOSE_LOOKUPS.get(
                                            filter_.lookup_expr, filter_.lookup_expr
                                        ).capitalize(),
                                    ]
                                    for lookup, filter_ in group_dct.items()
                                ]
                            )
                        ],
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
    selected_groups_with_filters = {}
    rest_groups = {}
    for lookup, filter_ in groups_with_filters.items():
        dct_to_add = rest_groups
        if lookup in selected_fields:
            dct_to_add = selected_groups_with_filters
        dct_to_add[lookup] = filter_
    select_filter_form = SelectFilterForm(groups_with_filters, filter_set.form.media, filters_data or None)
    return {
        "groups": rest_groups,
        "selected_groups": selected_groups_with_filters,
        "select_filter_form": select_filter_form,
    }


@register.simple_tag(takes_context=True)
def add_select_filter_form_to_context(context, filterset="filter"):
    context.dicts[0]["select_filter_form"] = _filters_by_groups(context, filterset)["select_filter_form"]
    return ""


@register.inclusion_tag("django_filters_groups/filters.html", takes_context=True)
def filters_by_groups(context, filterset="filter"):
    return _filters_by_groups(context, filterset)
