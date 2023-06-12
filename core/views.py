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


def shop_api(request):
    #realizamos solicitud al API
    response = requests.get('http://127.0.0.1:8000/api/productos/')    
    response2 = request.get('https://mindicador.cl/api/')    
    #page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1    
    #try:
    #    paginator = Paginator(productosAll, 5)
    #    productosAll = paginator.page(page)
    #except:
    #    raise Http404

    #transforma json para leerlo
    productos = response.json()
    monedas = response2.json()
    
    data = {
        'listado': productos,
        'monedas': monedas,        
    #    'paginator': paginator
        
    }
    return render(request, 'core/shop.html', data)


# LISTADO LOS PRODUCTOS EN SHOP
def shop(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    data = {
        'listaProducto' : productosAll
    }
    return render(request, 'core/shop.html', data)

# LISTADO DE PRODUCTOS EN INDEX
def index(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    data = {
        'listaProducto' : productosAll
    }
    return render(request, 'core/index.html', data)

#CRUD
def add(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST) # CAPTURAMOS LA INFO DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO producto VALUES()
            messages.success(request, "Producto agregado Correctamente")
        else:
            data["form"] = formulario
  
    return render(request, 'core/add-product.html', data)

def update(request, id):
    producto = Producto.objects.get(id=id) # SELECT CON WHERE (BUSCAR)
    data = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto) 
        if formulario.is_valid():
            formulario.save() # INSERT INTO producto VALUES()
            messages.success(request, "Producto modificado correctamente")
            return redirect(to="index")
        data['form'] = formulario # MOSTRAR EN LA VISTA LOS CAMBIOS

    return render(request, 'core/update-product.html', data)

def delete(request, id):
    producto = Producto.objects.get(id=id) # SELECT CON WHERE (BUSCAR)
    producto.delete()
    messages.success(request,"Producto eliminado correctamente")
    return redirect(to="index")

#----- PAGINAS DEFAULT

def about (request):
    return render (request, 'core/about.html')


def contact (request):
    return render (request, 'core/contact.html')

def news (request):
    return render (request, 'core/news.html')

def singlenews (request):
    return render (request, 'core/single-news.html')


#---COMPRAS

@login_required
def cart (request):
    response = requests.get('https://mindicador.cl/api/dolar')  
    moneda = response.json()
    valor_dolar = moneda['serie'][0]['valor'] #Valor dolar actual
    total_carrito = 10000 #aca se supone que suma los valores en el carrito
    valor = total_carrito/valor_dolar #precio transformado a dolar
    valor = round(valor,2) #se redondea valor a 2 decimales
    data = {
        'valor': valor
    }
    return render (request, 'core/cart.html')


@login_required
def checkout (request):
    return render (request, 'core/checkout.html')


def singleproduct (request):
    return render (request, 'core/single-product.html')

def datoscompra (request):
    return render (request, 'core/datos-compra.html')


def shop_api (request):
    return render (request, 'core/shop_api.html')


#---PERFIL

def micuenta (request):
    return render (request, 'core/mi-cuenta.html')





# ---REGISTRATION

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
    
