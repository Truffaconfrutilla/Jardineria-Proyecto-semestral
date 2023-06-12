from sys import maxsize
from typing import Any
from django.forms import ValidationError

#function
#clase

class MaxSizeFileValidator:

    def __init__(self, max_file_size = 90):
        self.max_file_size = max_file_size
    
    def __call__(self, value):
        size = value.size
        max.size = self.max_file_size * 10048576

        if size > maxsize:
            raise ValidationError(f"El tamaño maximo del archivo debe ser de {self.max_file_size}MB")
        
        return value