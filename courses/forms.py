from django import forms
from .models import MentorRequest


class MentorRequestForm(forms.ModelForm):

    class Meta:

        model = MentorRequest

        fields = ["challenge"]

        widgets = {
            "challenge": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": (
                        "Describe the issue you're facing..."
                    )
                }
            )
        }