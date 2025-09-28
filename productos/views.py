from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Producto

# Create your views here.


def index(request: HttpRequest):
    productos = Producto.objects.all()

    return render(
        request,
        'index.html',
        context={'productos': productos}
    )
