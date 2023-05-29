from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import viewsets
from .serializers import *
import requests

# Create your views here.

# view que se encarga de trasformar la data
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class TipoProductoViewset(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    
# LISTADO DE PRODUCTOS EN INDEX
def index(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto    
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1    
    try:
        paginator = Paginator(productosAll, 5)
        productosAll = paginator.page(page)
    except:
        raise Http404
    data = {
        'listado': productosAll,
        'paginator': paginator
    }
    return render(request, 'core/index.html', data)

def indexapi(request):
    #realizamos solicitud al API
    response = requests.get('http://127.0.0.1:8000/api/productos/')    
    #page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1    
    #try:
    #    paginator = Paginator(productosAll, 5)
    #    productosAll = paginator.page(page)
    #except:
    #    raise Http404

    data = response.json()
    #transforma json para leerlo
    
    data = {
        'listado': response,
    #    'paginator': paginator
    }
    return render(request, 'core/index.html', data)



#CRUD
#AGREGAR
def add(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST) # CAPTURAMOS LA INFO DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO producto VALUES()
            data['msj'] = "Producto guardado correctamente"
#ACTUALIZAR
def update(request, id):
    producto = Producto.objects.get(id=id) # SELECT CON WHERE (BUSCAR)
    data = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) 
        if formulario.is_valid():
            formulario.save() # INSERT INTO producto VALUES()
            messages.success(request, "Producto modificado correctamente")
            data['form'] = formulario # MOSTRAR EN LA VISTA LOS CAMBIOS

    return render(request, 'core/update-product.html', data)
#ELIMINAR
def delete(request, id):
    producto = Producto.objects.get(id=id) # SELECT CON WHERE (BUSCAR)
    producto.delete()

    return redirect(to="index")

def about (request):
    return render (request, 'core/about.html')

@login_required
def cart (request):
    return render (request, 'core/cart.html')

@login_required
def checkout (request):
    return render (request, 'core/checkout.html')

def contact (request):
    return render (request, 'core/contact.html')

def news (request):
    return render (request, 'core/news.html')

def shop (request):
    return render (request, 'core/shop.html')

def singlenews (request):
    return render (request, 'core/single-news.html')

def singleproduct (request):
    return render (request, 'core/single-product.html')




# REGISTRATION
def login (request):
    return render (request, 'registration/login.html')

def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request,f'Usuario {username} creado con éxito')
            return redirect('registercomplete')
    else:
        form = UserRegisterForm()
    context = {'form' : form }
    return render (request, 'registration/register.html',context)
    
def registercomplete (request):
    return render (request, 'registration/registercomplete.html')
    
