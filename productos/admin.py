from django.contrib import admin
from .models import Categoria, Producto


class CategoriaAdmin(admin.ModelAdmin):  # type: ignore
    exclude = ('creado_en', )
    list_display = ('id', 'nombre')


class ProductoAdmin(admin.ModelAdmin):  # type: ignore
    exclude = ('creado_en', )
    list_display = ('id', 'nombre', 'stock', 'creado_en')


# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
