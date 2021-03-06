from django import forms
from django.forms import Form, ChoiceField, CharField
from .models import UploadPdf, Jugdments
from django.forms import Form, ChoiceField, CharField

class UploadPdfForm(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ('document', )

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

class FilterForm(Form):
    FILTER_CHOICES = (
        ('processo', 'Processo'),
        ('orgao', 'Órgão'),
        ('classificacao', 'Classificação'),
        ('keyword', 'Palavra Chave'),
    )
    search = CharField(required=False)
    filter_field = ChoiceField(choices=FILTER_CHOICES)