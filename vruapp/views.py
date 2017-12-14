# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .models import TDR
from .forms import AnalysisForm

def handle_uploaded_file(file):
    cwd = os.getcwd()
    f=open(cwd + file,'r')
    tdrs = f.readlines()
    for tdr in tdrs:
        fields = tdr.split('|')
        record = fields[0]
        if record=='6021':
            imsi = fields[19]
            userAgent = fields[46]
            if userAgent !='' and (not '<' in userAgent and not '>' in userAgent):
                p = TDR(imsi = imsi, userAgent = userAgent)
                p.save()

def upload_tdr(request):
    if request.method == 'POST' and request.FILES['input-file']:
        myfile = request.FILES['input-file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        handle_uploaded_file(uploaded_file_url)
        cwd = os.getcwd()
        if os.path.isfile(cwd+uploaded_file_url):
            os.remove(cwd+uploaded_file_url)
        # allTDRs = TDR.objects.all()
        url=reverse('analysis')
        return HttpResponseRedirect(url)
    return render(request, 'index.html')

def analysis_tdr(request):

    form = AnalysisForm()
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            url =reverse('analysis')
            return HttpResponseRedirect(url)
    return render(request, 'analysis.html', {'form': form} )








# # Create your views here.
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .forms import UploadFileForm
#
# # Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
#
# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#                 destination.write(chunk)


#def get_date_from file()
#   f = open(cwd + '/TDR.log')
#   lines = f.readlines()
#   f.close()
#   for tdr in TDRS:
#      octets=ip.split('|')
#       a=field[0]
#       b=field[1]
