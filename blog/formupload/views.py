import logging
from datetime import datetime

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import TemplateView

from formupload.models import FileModel
from .forms import NameForm, UploadForm

logger = logging.getLogger('django')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'formupload/name.html', {'form': form})


class UploadFile(FormView):
    template_name = 'formupload/upload.html'
    form_class = UploadForm
    success_url = '/thanks/'


class FileUploadResult(TemplateView):
    template_name = 'formupload/thanks.html'


def handle_uploaded_file(f):
    file_name = str(int(datetime.now().timestamp()))
    with open(file_name, 'wb+') as destination:
        logging.debug("get file and save")
        for chunk in f.chunks():
            destination.write(chunk)


def get_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            file_model = FileModel()
            file_model.desc = "desc"
            file_model.file_name = 'null'
            file_model.file = form.cleaned_data['my_image']  # my_image
            file_model.file_length = 123
            file_model.save()

            logger.debug("save file to db")
            return HttpResponseRedirect('formupload/thanks/')
    else:
        form = UploadForm()
    return render(request, 'formupload/upload.html', {'form': form})
