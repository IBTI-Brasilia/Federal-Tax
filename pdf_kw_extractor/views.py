from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UploadPdf
from .forms import UploadPdfForm
from .utils import *
import textract
import re
import glob
import os


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
            list_of_files = glob.glob('/home/yan/repositorios/Federal-Tax/media/documents/*')
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

@login_required(login_url='/')
def list_keywords(request):
    jugdments = Jugdments.objects.filter().order_by('created_date')
    return render(request, 'pdf_kw_extractor/list_keywords.html', {'jugdments':jugdments})

@login_required(login_url='/')
def view_more(request, id):
    judgement = get_object_or_404(Jugdments, id =id)
    keywords = Keyword.objects.filter(judgment =judgement)
    return render(request, 'pdf_kw_extractor/view_more.html', {'judgement':judgement, 'keywords':keywords})