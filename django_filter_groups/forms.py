from django import forms


class SelectFilterForm(forms.Form):
    def __init__(self, groups_with_filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["filter"] = forms.ChoiceField(
            label="Select a filter",
            choices=[["", "------"]] + [[k, v["verbose_name"]] for k, v in groups_with_filters.items()],
        )

    @property
    def media(self):
        return forms.Media(js=("django_filter_groups/filter.js",), css={"screen": ("django_filter_groups/filter.css",)})
