# DJANGO PRODUCTLY

## A. Install Dependencies

```bash
pipenv install django
```

## B. Start Django Project

```bash
django-admin startproject <project-name> .
```

## C. Run Django Project

```bash
python manage.py runserver
```

## D. Create New App Template

```bash
python manage.py startapp productos
```

### D1. App Set Up

#### cd settings.py

Desde productos/apps.py se copia el nombre de la clase. En este caso 'ProductosConfig'

```python
INSTALLED_APPS = [
  ...,
  'productos.apps.ProductosConfig'
]
```

### D2. Add Urls

#### cd urls.py

```python
from django.contrib import admin
from django.urls import path, include  # Added 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls'))  # Added line
]
```

#### cd productos/urls.py (create file)

```python
from django.urls import path
from . import views

app_name = 'productos'
urlpatterns = [
    path('', views.index, name='index')
]
```

### D3. Add View

#### cd productos/views.py

```python
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest):
    return HttpResponse('Hola Mundo')
```

## E. Database

### E1. Define Models

#### cd productos/models.py

```python
from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    stock = models.IntegerField()
    puntaje = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # CASCADE: eliminar el producto
    # PROTECT: lanza un error
    # RESTRICT: solo elimina si no existen productos
    # SET_NULL: actualiza a valor nulo
    # SET_DEFAULT: asigna valor por defecto
    # categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=<value>)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre
```

### E2. Make Migrations

```bash
python manage.py makemigrations
```

### E3. Migrate

```bash
python manage.py migrate
```

## F. Admin

### F1. Create Admin User

Tras ingresar el siguiente comando se debe definir desde la terminal un nombre de usuario, un correo electrónico y una contraseña:

```bash
python manage.py createsuperuser
```

### F2. Register Models

#### cd productos/admin.py

```python
from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
```

### F3. Edit Model Admin View and Form Fields

#### cd productos/admin.py

```python
class CategoriaAdmin(admin.ModelAdmin):
    exclude = ('creado_en', )
    list_display = ('id', 'nombre')


class ProductoAdmin(admin.ModelAdmin):
    exclude = ('creado_en', )
    list_display = ('id', 'nombre', 'stock', 'creado_en')


# Register your models here.
```

## G. Views

### G1. Productos GET & JSON Response

#### cd productos/views.py

```python
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Producto

# Create your views here.


def index(request: HttpRequest):
    productos = Producto.objects.all().values()
    # productos = Producto.objects.filter(puntaje=5)
    # productos = Producto.objects.filter(puntaje_gte=3)
    # productos = Producto.objects.filter(puntaje_lte=3)
    # productos = Producto.objects.filter(puntaje_gt=3)
    # productos = Producto.objects.filter(puntaje_lt=3)
    # productos = Producto.objects.get(id=1)
    # productos = Producto.objects.get(pk=1)

    return JsonResponse(list(productos), safe=False)
```

### G2. HTML Template

#### cd productos/views.py

```python
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
```

#### cd productos/templates/index.html

```django
<h1>Productos</h1>

<table class="table">
  <thead>
    <tr>
      <th>Nombre</th>
      <th>Stock</th>
      <th>Puntaje</th>
      <th>Categoría</th>
    </tr>
  </thead>

  <tbody>
    {% for producto in productos %}
    <tr>
      <td>{{ producto.nombre }}</td>
      <td>{{ producto.stock }}</td>
      <td>{{ producto.puntaje }}</td>
      <td>{{ producto.categoria }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

### G3. Common Base Template

Creamos un html base que compartiran todos los demás templates de los diferentes aplicaciones. Y aprovechamos, en este ejemplo, para integrar bootstrap al HTML.

#### cd templates/base.html (create dir & file)

```django
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Productly</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous"
    />
  </head>
  <body>
    {% block content %}
    {% endblock %}
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
      crossorigin="anonymous"
    ></script>
  </body>
</html>
```

Crear el archivo no es suficiente. Para hacerlo disponible debemos agregar la ruta al archivo settings.py

#### cd productly/settings.py

```python
import os
# ...
TEMPLATES = [
    {
        # ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # ...
    },
]
# ...
```

Ahora modificamos el archivo index.html de la aplicación 'productos' para que extienda el template base:

#### cd productos/templates/index.html

```django
{% extends 'base.html' %}

{% block content %}
<!-- Nuestro código HTML aquí -->
{% endblock %}
```

### G4. Detalle Template Dynamic Route

#### cd productos/urls.py

```python
# ...

urlpatterns = [
   # ...
   path('<int:producto_id>', views.detalle, name='detalle')
]
```

#### cd productos/views.py
```python
# ...

def detalle(request: HttpRequest, producto_id: str):
    producto = Producto.objects.get(id=producto_id)

    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )
```

#### cd productos/templates/detalle.html
```django
{% extends 'base.html' %}

{% block content %}
<div>
  <h6>{{ producto.nombre }}</h6>
  <p>{{ producto.categoria }}</p>
  <p>{{ producto.stock }}</p>
  <p>{{ producto.puntaje }}</p>
  <p>{{ producto.creado_en }}</p>
</div>
{% endblock %}

```

### G5. 404 page for object not found

#### cd productos/views.py
```python
from django.shortcuts import render, get_object_or_404
# ...

def detalle(request: HttpRequest, producto_id: str):
    producto = get_object_or_404(Producto, id=producto_id)  # Cambio

    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )
```

### G6. Links

#### cd productos/index.html
```django
<!-- ... -->
 <td>
    <a href="{% url 'productos:detalle' producto.id %}">
      {{ producto.nombre }}
    </a>
  </td>
<!-- ... -->
```

## H. Forms

### H1. Form from Model Class

#### cd productly/settings.py
```python
# ...
INSTALLED_APPS = [
    # ...
    'django.forms', # Added line
    'productos.apps.ProductosConfig',
]
# ...
```

#### cd productos/forms.py (create file)

```python
from . import models
from django.forms import ModelForm


class ProductoForm(ModelForm):
    class Meta:
        model = models.Producto
        fields = ["nombre", "stock", "puntaje", "categoría"]

```

### H2. Form HTML

#### cd productos/templates/producto_form.html (created file)

```django
{% extends 'base.html' %}

{% block content %}

<form
  novalidate
  action="{% url 'productos:formulario' %}"
  method="post"
>
  {% csrf_token %}
  {{ form }}
  <input type="submit" value="Enviar" />
</form>

{% endblock %}
```

### H3. Views Integration

#### cd productos/views.py
```python
# ...
from django.http import HttpRequest, HttpResponseRedirect # New Import
from .forms import ProductoForm

# ...
def formulario(request: HttpRequest):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/productos')
    else:
        form = ProductoForm()

    return render(
        request,
        'producto_form.html',
        context={'form': form}
    )
```

#### cd productos/urls.py
```python
# ...
urlpatterns = [
    # ...
    path('formulario', views.formulario, name='formulario')
]
```

### H4. Form Customization

#### cd templates/form_snippet.html (create file)
```django
{% for field in form %}
    {{ field.label_tag }} {{ field }}
    {% for error in field.errors %}
        {{ error }}
    {% endfor %}
{% endfor %}
```

#### cd productly/settings.py
```python
# ...
from django.forms.renderers import TemplatesSetting

class CustomFormRenderer(TemplatesSetting):
    form_template_name = 'form_snippet.html'

FORM_RENDERER = "productly.settings.CustomFormRenderer"
# ...
```
