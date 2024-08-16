# files/forms.py

from django import forms
from .models import UploadedFile
from .models import Rating

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file','notes','genre']
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']