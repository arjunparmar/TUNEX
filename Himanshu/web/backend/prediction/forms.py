from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class TempForm(forms.Form):
    select_choices = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    recommend = forms.CharField(label="Click button for recommendation", widget=forms.RadioSelect(choices=select_choices))