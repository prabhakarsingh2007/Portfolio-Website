from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Your Name',
                'id': 'contact-name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Your Email',
                'id': 'contact-email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Subject',
                'id': 'contact-subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea', 
                'placeholder': 'Tell me about your project...',
                'id': 'contact-message',
                'rows': 5
            }),
        }
