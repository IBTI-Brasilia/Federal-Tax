from django import forms
from .models import UploadPdf, Jugdments


class UploadPdfForm(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ('document', )
        widgets = {
            'document': forms.FileInput(attrs={'style':'display: none;','class':'form-control-file', 'required': True})
        }

class JugdmentsForm(forms.ModelForm):
    class Meta:
        model = Jugdments
        fields = [
            'processo',
            'orgao',
            'ementa',
            'label_1',
            'label_2',
            'label_3',
        ]