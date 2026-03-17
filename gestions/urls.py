from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('mouvement/',views.mouvement, name='mouvement'),
    path('fournisseur/', views.supplier, name= 'supplier'),
    path('produit/',views.produit, name='produit'),
    path('productcreate/', views.product_create,  name='product_create'),
    path('supplier_create/', views.supplier_create, name='supplier_create'),
    path('category_create/', views.category_create, name='category_create'),
    path('mouvement_create/', views.mouvement_create, name='mouvement_create'),
    path('<int:id>/product_update/', views.product_update, name='product_update'),
    path('fournir/', views.fournir_create, name='fournir_create'),
    
    path('<int:pk>/product_delete/', views.product_delete, name='product_delete'),
    path('export/mouvements/', views.export_mouvements_csv, name='export_mouvements_csv' ),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="gestions/login.html"), name="login"),
    path("logout/", views.disconnect, name="disconnect"),

]