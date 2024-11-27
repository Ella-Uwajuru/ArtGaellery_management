from django import forms
from .models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['bio', 'contact', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself and your artistic journey...'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your preferred contact method'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://your-portfolio-website.com'
            })
        }
        help_texts = {
            'bio': 'Share your story, experience, and artistic vision.',
            'contact': 'How would you like potential clients to reach you?',
            'website': 'Optional: Link to your portfolio or personal website.'
        }

    def clean_website(self):
        """Ensure website URLs have proper format"""
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        return website

class ArtistSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search artists by name or bio...'
        })
    )

class ArtistPortfolioForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['bio', 'contact', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['bio'].widget.attrs['placeholder'] = 'Update your artist biography and statement'