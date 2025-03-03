from django import forms
from myapp.models import Order

class OrderForm(forms.ModelForm):
    """Form for placing orders"""
    class Meta:
        model = Order  # Based on Order model
        fields = ['client', 'product', 'num_units']  # Fields to include
        labels = {
            'num_units': 'Quantity',  # Custom label
            'client': 'Client Name'  # Custom label
        }
        widgets = {
            'client': forms.RadioSelect()  # Display clients as radio buttons
        }

class InterestForm(forms.Form):
    """Form for expressing interest in a product"""
    interested = forms.ChoiceField(
        widget=forms.RadioSelect,  # Yes/No radio buttons
        choices=[(1, 'Yes'), (0, 'No')]  # Values are 1 for Yes, 0 for No
    )
    quantity = forms.IntegerField(
        min_value=1,  # Must be at least 1
        initial=1,  # Default value is 1
        label='Quantity'
    )
    comments = forms.CharField(
        widget=forms.Textarea,  # Multi-line text box
        label='Additional Comments',
        required=False  
    )