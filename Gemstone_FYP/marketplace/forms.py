from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing

        fields = [
            "title",
            "description",
            "price",
            "weight",
            "color",
            "origin",
            "shape",
            "dimensions",
            "treatment",
            "certification",
            "quantity",
            "condition",
            "status",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Listing title",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe your gemstone",
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "weight": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "color": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "origin": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "shape": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "dimensions": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "treatment": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "certification": forms.TextInput(attrs={
                "class": "form-control",
            }),

            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "condition": forms.Select(attrs={
                "class": "form-select",
            }),

            "status": forms.Select(attrs={
                "class": "form-select",
            }),
        }




class ImageVerificationForm(forms.Form):

    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "gem-image-input",
                "accept": "image/*",
            }
        )
    )