from django.shortcuts import render
from django.http import HttpRequest
from .models import Producto

# Create your views here.


def index(request: HttpRequest):
    productos = Producto.objects.all()

    return render(
        request,
        'index.html',
        context={'productos': productos}
    )


def detalle(request: HttpRequest, producto_id: str):
    producto = Producto.objects.get(id=producto_id)

    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )
