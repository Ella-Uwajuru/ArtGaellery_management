from django import forms
from .models import Exhibition
from artworks.models import Artwork

class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ['title', 'description', 'start_date', 'end_date', 'artworks', 'location']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'artworks': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_artist:
            # Only show artworks that belong to the artist
            self.fields['artworks'].queryset = Artwork.objects.filter(artist__user=user)
        
        # Add help texts
        self.fields['start_date'].help_text = 'Select the exhibition start date'
        self.fields['end_date'].help_text = 'Select the exhibition end date'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date.")
            
            # Check for overlapping exhibitions
            overlapping = Exhibition.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            )
            
            if self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            
            if overlapping.exists():
                raise forms.ValidationError(
                    "There is already an exhibition scheduled during these dates."
                )

        return cleaned_data