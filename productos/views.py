from django.shortcuts import render, get_object_or_404
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
    producto = get_object_or_404(Producto, id=producto_id)

    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )
