from django.shortcuts import render, redirect

# Create your views here.
from Site.forms import AjaxSavePhoto, AjaxPhotoFeed
from Site.models import Photo, Post, Comment


def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return redirect('login', )


def ajaxsavephoto(request):
    ajax = AjaxSavePhoto(request.POST, request.user)
    context = {'ajax_output': ajax.output()}
    return render(request, 'ajax.html', context)


def ajaxphotofeed(request):
    ajax = AjaxPhotoFeed(request.GET, request.user)
    context = {'ajax_output': ajax.output()}
    return render(request, 'ajax.html', context)

