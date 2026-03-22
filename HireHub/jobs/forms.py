from django import forms
from .models import Job_Create

class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job_Create
        fields = ['title', 'description', 'location', 'salary', 'company']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title...',
                'required': True,
            }),

            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name...',
                'required': True,
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location...',
                'required': True,
            }),

            'salary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. $50,000 - $80,000',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the job role, responsibilities, and requirements...',
                'rows': 5,
                'required': True,
            }),
        }

    # 🔥 Add automatic error styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'