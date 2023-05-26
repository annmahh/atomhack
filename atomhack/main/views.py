import shutil

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import models
from django.shortcuts import render, redirect
from .forms import UploadFileForm, LoginUserForm
import zipfile
from . import scripts
from .scripts.collect_packages import collect_packages
from django.conf import settings
import os


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'main/index.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'main/profile.html', {'form': form})


def upload(request):
    return render(request, '<h4>Upload</h4>')


def handle_uploaded_file(f):
    with zipfile.ZipFile(f, 'r') as zip_file:
        zip_file.extractall('main/folders/input')
#    with open(f, 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'main/reg.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('index')


def uploadFile(request):
    if request.method == "POST":
        # получение
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # сохранение в базу
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    file = os.path.join(settings.MEDIA_ROOT, str('Uploaded Files\\example.zip'))
    path = os.path.join(settings.MEDIA_ROOT, 'Unzipped Files')
    save_path = os.path.join(settings.MEDIA_ROOT, 'Downloaded Files')

    with zipfile.ZipFile(file, 'r') as zip_file:
        zip_file.extractall(path)
    collect_packages(path+'\\example', save_path)

    return render(request, "main/upload-file.html", context = {
        "files": documents
    })