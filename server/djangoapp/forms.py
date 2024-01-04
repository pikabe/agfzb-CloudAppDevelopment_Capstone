# forms.py
from django import forms
from .models import DealerReview, CarModel

class ReviewForm(forms.ModelForm):
    class Meta:
        model = DealerReview
        fields = ['name', 'purchase', 'review', 'purchase_date', 'car_model', 'car_year', 'sentiment']

    # Add fields for car selection
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.values_list('name', flat=True).distinct(), empty_label=None)
    car_year = forms.ModelChoiceField(queryset=CarModel.objects.values_list('year', flat=True).distinct(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Customize the labels for the car fields
        self.fields['car_model'].label = 'Car Model'
        self.fields['car_year'].label = 'Car Year'
