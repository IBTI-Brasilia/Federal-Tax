from django import forms
from .models import UploadPdf


class UploadPdfForm(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ('document', )
        widgets = {
            'document': forms.FileInput(attrs={'style':'display: none;','class':'form-control', 'required': True})
        }
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['document'].widget.attrs.update({'position':'absolute', 'height':'1px', 'left':'0px', 'right':'0px', 'bottom':'0px', 'left':'0px', 'background': '#D3D8DD'})
