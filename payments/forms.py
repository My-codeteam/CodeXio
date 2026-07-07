from django import forms
from .models import Payment

class PaymentProofForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ["receipt"]