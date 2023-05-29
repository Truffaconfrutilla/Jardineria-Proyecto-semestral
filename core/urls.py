from django.urls import path, include
from .views import *
from . import views
from django. contrib.auth.views import LoginView,LogoutView
from rest_framework import routers

#Para crear el api
router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tipo_productos', TipoProductoViewset)

urlpatterns = [
    path('', index, name ="index"),
    path('indexapi', indexapi, name ="indexapi"),
    path('about/', about, name ="about"),
    path('cart/', cart, name ="cart"),
    path('checkout/', checkout, name ="checkout"),
    path('contact/', contact, name ="contact"),   
    path('news', news, name ="news"),
    path('shop', shop, name ="shop"),
    path('singlenews', singlenews, name ="singlenews"),
    path('singleproduct', singleproduct, name ="singleproduct"),

    #register
    path('login/', login, name ="login"),
    path('register/', views.register, name ="register"),
    path('registercomplete/', views.registercomplete, name ="registercomplete"),

    #crud
    path('add/', add, name="add"),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    #
    path('api/', include(router.urls)),
]
