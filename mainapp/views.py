from django.shortcuts import render


def index(request):
    return render(request, 'main_site/index.html', {})


def about(request):
    return render(request, 'main_site/about.html', {})