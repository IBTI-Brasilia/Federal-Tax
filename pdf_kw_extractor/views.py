from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UploadPdf
from .forms import UploadPdfForm, JugdmentsForm
from .utils import *
import textract
import re
import glob
import os


@csrf_exempt 

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            list_of_files = glob.glob('/home/camila/Desktop/projetos/ibti/Federal-Tax/media/documents/*')
            lastest_file = max(list_of_files, key=os.path.getctime)
            text = textract.process(lastest_file, method='pdfminer').decode('utf-8')
            paragraphs = re.split('\n\n', text)
            clean_paragraphs = cleanner(text)
            occurrences = occurrences_keywords(clean_paragraphs)
            save_db(clean_paragraphs, lastest_file, occurrences)
            return redirect('/')
    else:
        form = UploadPdfForm()
    return render(request, 'pdf_kw_extractor/upload_pdf.html', {
            'form':form,
        })

def list_keywords(request):
    jugdments = Jugdments.objects.filter().order_by('created_date')
    return render(request, 'pdf_kw_extractor/list_keywords.html', {'jugdments':jugdments})

def view_more(request, id):
    judgement = get_object_or_404(Jugdments, id =id)
    keywords = Keyword.objects.filter(judgment =judgement)
    form = JugdmentsForm(request.POST)
    if request.method == 'POST' and 'update' in request.POST:
        if form.is_valid():
            judgement.save()
            return redirect('list_keywords')
    return render(request, 'pdf_kw_extractor/view_more.html', {'judgement':judgement, 'keywords':keywords})