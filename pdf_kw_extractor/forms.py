from django import forms
from .models import UploadPdf


class UploadPdfForm(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ('document', )
        widgets = {
            'document': forms.FileInput(attrs={'style':'display: none;','class':'form-control', 'required': True})
        }