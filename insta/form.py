from croppie.fields import CroppieField
from django import forms

from insta.models import Quote


class AddQuote(forms.ModelForm):
    img = CroppieField(
        options={
            'viewport': {
                'width': 100,
                'height': 100,
                'type': 'circle',
            },
            'boundary': {
                'width': 150,
                'height': 150,
            },
            'showZoomer': True,
        },
    )

    class Meta:
        model = Quote
        fields = ('description', 'author', 'position', 'img')
