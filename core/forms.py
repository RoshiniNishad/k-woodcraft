from django import forms
from .models import ContactMessage
from .models import Payment
from datetime import date

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["location", "delivery_date", "advance_payment"]

    def __init__(self, *args, **kwargs):
        self.total_amount = kwargs.pop("total_amount", None)
        super().__init__(*args, **kwargs)

    def clean_advance_payment(self):
        advance = self.cleaned_data.get("advance_payment")
        if self.total_amount and advance < (0.5 * float(self.total_amount)):
            raise forms.ValidationError("Advance must be at least 50% of the total amount.")
        return advance

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date < date.today():
            raise forms.ValidationError("Delivery date cannot be in the past.")
        return delivery_date