from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'  # all fields

    
    # customised ImageField form
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    # overriding the init method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # categories by their visible_names
        categories = Category.objects.all()
        # list comprehension for adding items to a list
        visible_names = [(c.id, c.get_visible_name()) for c in categories]

        # to use the visible_names in the select dropdown
        self.fields['category'].choices = visible_names
        # adding css classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
