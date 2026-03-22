from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant_name', 'applicant_email', 'resume', 'cover_letter']
        widgets = {
            'applicant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'applicant_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Cover Letter (optional)'
            }),
        }

    def clean_applicant_email(self):
        email = self.cleaned_data.get('applicant_email')
        return email.lower() if email else email