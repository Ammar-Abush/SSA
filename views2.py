import magic
import os

from django.shortcuts import render
from django.conf import settings
# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Document
from .forms import DocumentForm


def delete(request, pk):
    if request.method == 'POST':
        file = get_object_or_404(Document, pk=pk)
        file.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, file.docfile.name))
    return HttpResponseRedirect(reverse("index"))
def index(request):
    if request.method == 'POST':
        print("Othman is hungry")
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            valid_mime_types = [
                'application/msword', 'text/plain',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-excel', 'image/jpeg', 'image/png',
                'application/vnd.oasis.opendocument.text',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/pdf',
                'application/gzip' #xournalpp,
                
            ]
            mime = magic.Magic(mime=True)
            files = request.FILES.getlist('docfile')
            for uploaded_file in files:
                mime_type = mime.from_buffer(uploaded_file.read())
                print(mime_type)
                uploaded_file.seek(0)
                print(mime_type)
                if mime_type in valid_mime_types:
                    newdoc = Document(docfile=uploaded_file)
                    newdoc.save()
                else:
                    print("HIIII")
                    return render(request, "FileUploadServer/error.html", {'error': "Some files uploaded are don't have supported types"})
            return HttpResponseRedirect(reverse('index'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'FileUploadServer/index.html', {'documents': documents, 'form': form})

