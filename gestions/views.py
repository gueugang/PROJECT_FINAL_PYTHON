from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Group
from .models import Administrateur, Supplier, Product,Magasinier
from .forms import  SupplierForm, ProductForm, UserRegisterForm, CategoryForm, FournirForm, MouvementForm
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'gestions/index.html')
@login_required
def mouvement(request):
    
    return render(request, 'gestions/mouvement.html')

@login_required
def produit(request,):
    products = Product.objects.all().order_by('-created_at')
    
    return render(request, 'gestions/produit.html', {'products':products})

@login_required
def supplier(request):
    suppliers = Supplier.objects.all().order_by('-created_at')
    return render(request, 'gestions/fournisseur.html', {'suppliers': suppliers})

@login_required
def product_create(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('produit')
    return render(request, 'gestions/produit_form.html', {'form': form, 'title': 'Nouveau Produit'})   

@login_required
def supplier_create(request):
    form = SupplierForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('supplier')
    return render(request, 'gestions/supplier_form.html', {'form': form, 'title': 'Nouveau Fournisseur'})

@login_required

def product_update(request, id):
    product = get_object_or_404(Product, id= id)
    
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('produit')
    return render(request, "gestions/product_update.html", {"form": form, "titlt": "Modifier un Produit"})

def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
         form.save()
         return redirect('produit')
    return render(request, "gestions/category_create.html", {"form": form, "title":"Category"})


@login_required
def fournir_create(request):
    form = FournirForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('supplier')
    return render(request, 'gestions/fournir_create.html', {'form':form, 'title':'Relier un Fournisseur a un Produit'})

@login_required
def mouvement_create(request):
    form = MouvementForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('supplier')
    return render(request, 'gestions/category_create.html', {'form':form, 'title':'Enregistree un movement'})

# creation des utilisateur : magasinier et administrateurs
# @login_required
# def create_magasinier(request):
#     if request.method == "POST":

#         user = User.objects.create_user(
#             username=request.POST['username'],
#             email=request.POST['email'],
#             password=request.POST['password']
#         )

#         Magasinier.objects.create(
#             user=user,
#             adress=request.POST['adress']
#         )

#         group = Group.objects.get(name='Magasinier')
#         user.groups.add(group)

#         return redirect('login')

#     return render(request,'create_magasinier.html')

# @login_required
# def create_admin(request):

#     if request.method == "POST":

#         user = User.objects.create_user(
#             username=request.POST['username'],
#             email=request.POST['email'],
#             password=request.POST['password'],
#             role =  request.POST['role']
#         )

#         Administrateur.objects.create(
#             user=user,
#             adress=request.POST['adress']
#         )

#         group = Group.objects.get(name='Administrateur')
#         user.groups.add(group)

#         return redirect('login')

#     return render(request,'create_admin.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Création de l'utilisateur
            user = form.save()

            name = form.cleaned_data.get("name")
            adress = form.cleaned_data.get("adress")
            role = form.cleaned_data.get("role")

            # Création du profil selon le rôle
            if role == "Magasinier":
                Magasinier.objects.create(user=user, name=name, adress=adress)
            else:
                Administrateur.objects.create(user=user, name=name, adress=adress, role=role)

            # Ajouter au groupe
            group = Group.objects.get(name=role)
            user.groups.add(group)

            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "gestions/register.html", {"form": form, "title":"Creer un Nouveau Compte"})

def profil(request):

    if hasattr(request.user, 'magasinier'):
        profil = request.user.magasinier
        role = "Magasinier"

    elif hasattr(request.user, 'administrateur'):
        profil = request.user.administrateur
        role = "Administrateur"

    else:
        profil = None
        role = "Utilisateur"

    return render(request, "base.html", {"profil": profil, "role": role})

@login_required
def disconnect(request):
    logout(request)
    return redirect("index")