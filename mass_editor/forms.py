from django import forms
from .service.fields import getAllFields

class CustomFieldForm(forms.Form):
    options = forms.MultipleChoiceField(
        choices=getAllFields,
        widget=forms.SelectMultiple,
        required=True,
        label="Custom Fields"
    )
