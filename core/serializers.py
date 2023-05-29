# se va a encargar de convertir los archivos a json
from .models import *
from rest_framework import serializers

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    #agregar claves foraneas fk
    tipo = TipoProductoSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

