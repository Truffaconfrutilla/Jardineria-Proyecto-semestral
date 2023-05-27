from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# PARA CREAR UN TEMPLATE DE UN FORMULARIO
class ProductoForm(ModelForm):

    nombre = forms.CharField(min_length=4,widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=200,widget=forms.Textarea(attrs={"rows":4}))

    class Meta:
        model = Producto
        #fields = ['nombre','precio','stock','descripcion','tipo']
        fields = '__all__'

        widgets = {
            'vencimiento' : forms.SelectDateWidget(years=range(1960,2024))
        }

# FORM REGISTRO

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Eléctronico', widget= forms.EmailInput)
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme Contraseña',widget=forms.PasswordInput)

    class Meta:
        model= User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields}

