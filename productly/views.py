from django.shortcuts import render
from django.http import HttpRequest


def inicio(request: HttpRequest):
    return render(
        request,
        "inicio.html"
    )
