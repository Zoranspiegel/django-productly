# DJANGO PRODUCTLY

## 01. Install Dependencies

```bash
pipenv install django
```

## 02. Start Django Project

```bash
django-admin startproject <project-name> .
```

```bash
python manage.py runserver
```

```bash
python manage.py startapp productos
```

#### cd settings.py

```python
INSTALLED_APPS = [
  ...,
  'productos.apps.ProductosConfig'
]
```

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

#### cd productos/views.py

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hola Mundo')
```

```bash

```
