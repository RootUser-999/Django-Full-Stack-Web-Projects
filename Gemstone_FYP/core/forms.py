from django import forms
from .models import imageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = imageUpload
        fields = ['gem_image']

        widgets = {
            'gem_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            )
        }