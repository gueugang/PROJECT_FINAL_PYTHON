from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Group
from .models import Administrateur, Supplier, Product,Magasinier, Category, Mouvement, Fournir
from .forms import  SupplierForm, ProductForm, UserRegisterForm, CategoryForm, FournirForm, MouvementForm
from django.contrib.auth import logout
from django.db.models import Sum, Count

import csv
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'gestions/index.html')
@login_required
def mouvement(request):
    type_mvt = request.GET.get("type")
    total_entree = Mouvement.objects.filter(type="entree").aggregate(total_ent=Sum('quantity'))
    total_sortie = Mouvement.objects.filter(type="sortie").aggregate(total_sort=Sum('quantity'))
    difference = total_entree["total_ent"] - total_sortie["total_sort"]
    if type_mvt == "entree":
        mouvements = Mouvement.objects.filter(type="entree")
    elif type_mvt== "sortie":
        mouvements = Mouvement.objects.filter(type="sortie")
    else:
        mouvements = Mouvement.objects.all().order_by('-created_at')
    return render(request, 'gestions/mouvement.html', {'mouvements':mouvements, 'difference':difference, 'total_entree':total_entree["total_ent"], 'total_sortie':total_sortie["total_sort"]})

@login_required
def produit(request):
    products = Product.objects.all().order_by('-created_at')
    fournirs = Fournir.objects.all()
    category = request.GET.get("category")
    
    if category:
        products = products.filter(category_id=category)
 
    categories = Category.objects.all()
    print(categories)
    return render(request, 'gestions/produit.html', {'products':products, 'fournir': fournirs, 'categories': categories})

@login_required
def supplier(request):
    fournirs = Fournir.objects.values('supplier').annotate(total = Count('supplier'))
    total = Fournir.objects.all().count()
    print(fournirs)
    suppliers = Supplier.objects.all().order_by('-created_at')
    return render(request, 'gestions/fournisseur.html', {'suppliers': suppliers,'fournirs':fournirs, 'total':total})

@login_required
def product_create(request):
    form = ProductForm(request.POST, request.FILES)
    print(form.is_valid())
    if form.is_valid():
        form.save()
        return redirect('produit')
    print(form.is_valid())
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
    product = get_object_or_404(Product, pk=id)
    
    print(product)
    
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    print(form.is_valid())
    if form.is_valid():
        form.save()
        return redirect('produit')
    print(form.is_valid())
    return render(request, "gestions/product_update.html", {"form": form, "title": "Modifier un Produit"})

@login_required
def supplier_update(request, id):
    supplier = get_object_or_404(Supplier, id= id)
    
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('supplier')
    return render(request, "gestions/supplier_create.html", {"form": form, "titlt": "Modifier les Informations Sur un Fournisseur"})

@login_required
def mouvement_update(request, id):
    mouvement = get_object_or_404(Mouvement, id= id)
    
    form = MouvementForm(request.POST or None, instance=mouvement)
    if form.is_valid():
        form.save()
        return redirect('mouvement')
    return render(request, "gestions/produit_form.html", {"form": form, "titlt": "Modifier un Mouvement"})

@login_required
def category_update(request, id):
    category = get_object_or_404(Category, id= id)
    
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('produit')
    return render(request, "gestions/produit_form.html", {"form": form, "titlt": "Modifier une Category"})

@login_required
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
         form.save()
         return redirect('produit')
    return render(request, "gestions/category_create.html", {"form": form, "title":"Creer une Category"})


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
        return redirect('mouvement')
    return render(request, 'gestions/produit_form.html', {'form':form, 'title':'Enregistree un movement'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('produit')
    return render(request, 'gestions/confirmation_delete.html', {'product': product, 'title':'le produit'})

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

#---------test de mail

from django.core.mail import send_mail
from django.conf import settings

def envoyer_mail(request):
    send_mail(
        "Sujet du mail",
        "Bonjour, ceci est un mail envoyé depuis Django",
        settings.EMAIL_HOST_USER,
        ["ngouneloic562@gmail.com"],
        fail_silently=False,
    )
    
    
def export_mouvements_csv(request):
    # Création de la réponse HTTP avec type CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mouvements.csv"'

        writer = csv.writer(response)

        # En-têtes du fichier
        writer.writerow(['product', 'dateMvt', 'quantity', 'valide', 'type', 'magasinier', 'administrateur'])

        # Données
        mouvements = Mouvement.objects.all()

        for mouvement in mouvements:
            writer.writerow([
                mouvement.product,
                mouvement.dateMvt,
                mouvement.quantity,
                mouvement.valide,
                mouvement.type,
                mouvement.magasinier,
                mouvement.administrateur
            ])

        return response