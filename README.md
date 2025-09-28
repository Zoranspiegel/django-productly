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

urlpatterns = [
    path('', views.index, name='index')
]
```

### D3. Add View

#### cd productos/views.py

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hola Mundo')
```

### D4. Define Models

#### cd productos/models.py

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)


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
```

### D5. Make Migrations
```bash
python manage.py makemigrations
```

### D6. Migrate
```bash
python manage.py migrate
```
