from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UploadPdf
from .forms import UploadPdfForm, JugdmentsForm
from .utils import *
import textract
import re
import glob
import os
from django.conf import settings


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
    form = JugdmentsForm(request.POST, instance=judgement)
    if request.method == 'POST' and 'update' in request.POST:
        #if form.is_valid():
        processo = request.POST.get("processo", None)
        orgao = request.POST.get("orgao", None)
        ementa = request.POST.get("ementa", None)
        if processo:
            judgement.processo = processo
        if orgao:
            judgement.orgao = orgao
        if ementa:
            judgement.ementa = ementa
        judgement.save()
        return redirect('list_keywords')
    else:
        form = JugdmentsForm(instance=judgement)
    return render(request, 'pdf_kw_extractor/view_more.html', {'judgement':judgement, 'keywords':keywords})

def delete_process(request, id):
    try:
        process_sel = Jugdments.objects.get(id = id)
    except Jugdments.DoesNotExist:
        return redirect('/')
    process_sel.delete()
    return redirect('/')

def download_pdf(request, id):
    judgement = get_object_or_404(Jugdments, id =id)
    title = judgement.title
    head_tail = os.path.split(title)
    file_ = 'documents/' + head_tail[1]
    file_path = os.path.join(settings.MEDIA_ROOT, file_)    
    if os.path.exists(file_path):    
        with open(file_path, 'rb') as fh:    
            response = HttpResponse(fh.read(), content_type="application/pdf")    
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)    
            return response
