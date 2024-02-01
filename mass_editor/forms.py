from django import forms

class CustomFieldForm(forms.Form):
    options = forms.MultipleChoiceField(
        choices=[
            ('low_priority', 'Low Priority'),
            ('medium_priority', 'Medium Priority'),
            ('high_priority', 'High Priority'),
            ('todo', 'To Do'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('bug', 'Bug'),
            ('feature_request', 'Feature Request'),
            ('documentation', 'Documentation'),
            ('maintenance', 'Maintenance'),
            ('research', 'Research'),
            ('design', 'Design'),
        ],
        widget=forms.SelectMultiple,
        required=True,
        label="Custom Fields"
    )
