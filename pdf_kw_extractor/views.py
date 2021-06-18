from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UploadPdf
from .forms import UploadPdfForm, JugdmentsForm, FilterForm
from .utils import *
import textract
import re
import glob
import os
from django.conf import settings
from django.views.generic import ListView

@csrf_exempt 

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/upload_pdf/')
    return render(request, 'pdf_kw_extractor/login.html', {})

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('/upload_pdf')
        else:
            messages.error(request, 'Usuário ou senha inválido.')
    return redirect('/')

def logout_request(request):
    logout(request)
    messages.info(request, "Usuário deslogado com sucesso!")
    return redirect("/")

@login_required(login_url='/')
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            list_of_files = glob.glob('./media/documents/*')
            lastest_file = max(list_of_files, key=os.path.getctime)
            text = textract.process(lastest_file, method='pdfminer').decode('utf-8')
            paragraphs = re.split('\n\n', text)
            clean_paragraphs = cleanner(text)
            occurrences = occurrences_keywords(clean_paragraphs)
            save_db(clean_paragraphs, lastest_file, occurrences)
            messages.add_message(request, messages.SUCCESS, 'Upload feito com sucesso!')
            return redirect('/')
    else:
        form = UploadPdfForm()
    return render(request, 'pdf_kw_extractor/upload_pdf.html', {
            'form':form,
        })

@login_required(login_url='/')
def list_keywords(request):
    jugdments = Jugdments.objects.filter().order_by('created_date')
    return render(request, 'pdf_kw_extractor/list_keywords.html', {'jugdments':jugdments})

@login_required(login_url='/')
def view_more(request, id):
    judgement = get_object_or_404(Jugdments, id =id)
    keywords = Keyword.objects.filter(judgment =judgement)
    form = JugdmentsForm(request.POST, instance=judgement)
    if request.method == 'POST' and 'update' in request.POST:
        #if form.is_valid():
        processo = request.POST.get("processo", None)
        orgao = request.POST.get("orgao", None)
        ementa = request.POST.get("ementa", None)
        label_1 = request.POST.get("arquivos", None)
        label_2 = request.POST.get("subarq", None)
        label_3 = request.POST.get("lastarq", None)
        if processo:
            judgement.processo = processo
        if orgao:
            judgement.orgao = orgao
        if ementa:
            judgement.ementa = ementa
        if label_1:
            judgement.label_1 = label_1
        if label_2:
            judgement.label_2 = label_2
        if label_3:
            judgement.label_3 = label_3
        judgement.save()
        return redirect('list_keywords')
    else:
        form = JugdmentsForm(instance=judgement)
    return render(request, 'pdf_kw_extractor/view_more.html', {'judgement':judgement, 'keywords':keywords})

@login_required(login_url='/')
def delete_process(request, id):
    try:
        process_sel = Jugdments.objects.get(id = id)
    except Jugdments.DoesNotExist:
        return redirect('list_keywords')
    title = process_sel.title
    process_sel.delete()
    head_tail = os.path.split(title)
    file_ = 'documents/' + head_tail[1]
    try:
        pdf_file = UploadPdf.objects.get(document = file_)
    except UploadPdf.DoesNotExist:
        return redirect('list_keywords')
    pdf_file.delete()
    file_path = os.path.join(settings.MEDIA_ROOT, file_)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('list_keywords')

@login_required(login_url='/')
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

class HomeView(ListView):
    model = Jugdments
    template_name = 'pdf_kw_extractor/home.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        # Do your filter and search here
        if filter_field == 'orgao':
            return Jugdments.objects.filter(orgao=query)
        if filter_field == 'processo':
            return Jugdments.objects.filter(processo=query)
        if filter_field == 'classificacao':
            try:
                classif = Jugdments.objects.filter(label_1=query)
                return classif
            except Jugdments.DoesNotExist:
                try:
                    classif = Jugdments.objects.filter(label_2=query)
                    return classif
                except Jugdments.DoesNotExist:
                    classif = Jugdments.objects.filter(label_3=query)
                    return classif

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context