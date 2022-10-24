from django import forms
from django.conf import settings


class SelectFilterForm(forms.Form):
    def __init__(self, groups_with_filters, filterset_media, *args, **kwargs):
        self.filterset_media = filterset_media
        super().__init__(*args, **kwargs)
        self.fields["filter"] = forms.ChoiceField(
            required=False,
            label=getattr(settings, "FILTERS_GROUPS_SELECT_FILTER_FORM_LABEL", "Select a filter"),
            choices=[["", "------"]] + [[k, v["verbose_name"]] for k, v in groups_with_filters.items()],
        )

    @property
    def media(self):
        return self.filterset_media + forms.Media(
            css={"screen": ("django_filters_groups/filter.css",)},
            js=("django_filters_groups/filter-defaults.js", "django_filters_groups/filter.js"),
        )
