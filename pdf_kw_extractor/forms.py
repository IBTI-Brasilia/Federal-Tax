from django import forms
from .models import UploadPdf, Jugdments
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, HTML
from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    FieldWithButtons,
    InlineCheckboxes,
    InlineRadios,
    PrependedAppendedText,
    PrependedText,
    StrictButton,
    Tab,
    TabHolder,
)


class UploadPdfForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             #Field('', ButtonHolder('file', "Browse", css_class="fas fa-arrow-circle-up", template="/home/camila/Desktop/projetos/ibti/Federal-Tax/pdf_kw_extractor/templates/pdf_kw_extractor/file_input.html", css_id="id_file")),
#             Field('document',
#                 style = 'opacity: 5; width: 12px; height: 0.1px;',
#                 css_id = 'file-input',
#                 #template="/home/camila/Desktop/projetos/ibti/Federal-Tax/pdf_kw_extractor/templates/pdf_kw_extractor/file_input.html"
#                 #type="hidden"
#                 )
#         )
    class Meta:
        model = UploadPdf
        fields = ('document', )
        # widgets = {
        #     'document': forms.FileInput(attrs={'style':'display: none;','class':'form-control-file', 'id':'hello', 'value': 'Upload', 'required': True})
        # }

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