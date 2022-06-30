from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Using the UserProfile model and excluding only the user field
    since we never want to edit this
    """

    class Meta:
        model = UserProfile
        exclude = (
            'user',
        )

    def __init__(self, *args, **kwargs):
        """
        Overriding the init method inorder to make the form very customizable

        -calling the default init method to set up the form as it would be
        -defines a dictionary of placeholders for the form fields (defaults)
        (no name or email on this form since its from user model)
        -sets autofocus to the default_phone_number field so the cursor starts 
        there
        -iterates through the form fields to add * to the required fields,
        setting the field's placeholder adding the appropriate css classes
        to keep it styled like th rest of the site
        -removes the default field label
        """

        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address_1': 'Street Address 1',
            'default_street_address_2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
