from django import forms
from django.utils.translation import gettext_lazy as _


class SelectFilterForm(forms.Form):
    def __init__(self, groups_with_filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["filter"] = forms.ChoiceField(
            required=False,
            label=_("Select a filter"),
            choices=[["", "------"]] + [[k, v["verbose_name"]] for k, v in groups_with_filters.items()],
        )

    @property
    def media(self):
        return forms.Media(
            css={"screen": ("django_filters_groups/filter.css",)},
            js=("django_filters_groups/filter-defaults.js", "django_filters_groups/filter.js"),
        )
