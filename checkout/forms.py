from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Using the Order model and with only the editable non-auto generated fields
    avaliable
    """

    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address_1',
            'street_address_2',
            'town_or_city',
            'postcode',
            'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Overriding the init method inorder to make the form very customizable

        -calling the default init method to set up the form as it would be
        -defines a dictionary of placeholders for the form fields
        -sets autofocus to the full_name field so the cursor starts there
        -iterates through the form fields to add * to the required fields,
        setting the field's placeholder adding the 'stripe-style-input' css
        class
        -removes the default field label
        """

        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address_1': 'Street Address 1',
            'street_address_2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
