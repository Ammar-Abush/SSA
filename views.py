import magic, pprint, mimetypes
import os, subprocess

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
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            valid_mime_types = [
                'application/msword', 'text/plain',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-excel', 'image/jpeg', 'image/png',
                'application/vnd.oasis.opendocument.text',
                'application/gzip' #xournalpp
            ]
            mime = magic.Magic(mime=True)
            files = request.FILES.getlist('docfile')
            for uploaded_file in files:
                mime_type = mime.from_buffer(uploaded_file.read())
                uploaded_file.seek(0)
                print(mime_type)
                if mime_type in valid_mime_types:
                    newdoc = Document(docfile=uploaded_file)
                    newdoc.save()

                    file_path = os.path.join(settings.MEDIA_ROOT, newdoc.docfile.name)
                    file_dir = os.path.dirname(file_path)

                    
                    subprocess.Popen(["swaymsg", "exec", f"xdg-open {file_path}"])
                else:
                    print("HIIII")
                    return render(request, "upload/error.html", {'error': "Some files uploaded are don't have supported types"})
            return HttpResponseRedirect(reverse('index'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'upload/index.html', {'documents': documents, 'form': form})
