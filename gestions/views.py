from datetime import timedelta
import json

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Group
from .models import Administrateur, Supplier, Product,Magasinier, Category, Mouvement, Fournir
from .forms import  SupplierForm, ProductForm, UserRegisterForm, CategoryForm, FournirForm, MouvementForm, LoginForm
from django.contrib.auth import logout, authenticate, login
from django.db.models import Sum, Count, F
from django.contrib import messages
from django.utils import timezone

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
    else:
        products = Product.objects.all().order_by('-created_at')
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

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('produit')
    return render(request, 'gestions/confirmation_delete.html', {'product': product, 'title':'le produit'})

from django.db import transaction
@transaction.atomic
def valider_mouvement(request, pk):
    mouvement = Mouvement.objects.select_for_update().get(pk=pk)
    
    if mouvement.valide:
        messages.warning(request, "Ce mouvement a déjà été validé !")
        return redirect('mouvement')  # déjà traité
    
    product = mouvement.product
    print("====================================================")
    print(mouvement.type)
    if mouvement.type == 'entree':
        product.stockQuantity += mouvement.quantity
        
    elif mouvement.type == 'sortie':
        print("entrer jfkl")
        if product.stockQuantity < mouvement.quantity:
            
            messages.error(request, "Stock insuffisant !")
            return redirect('mouvement')

        product.stockQuantity -= mouvement.quantity

    product.save()

    mouvement.valide = True
    mouvement.save()
    messages.success(request, f"Mouvement validé pour {product.name} !")
    return redirect('mouvement')


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

def login_in(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('produit')  # change selon ton projet
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'gestions/login.html', {'form': form})
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
    
@login_required
def dashboard(request):
    # Produits
    products = Product.objects.all()

    # Stock total
    total_stock = products.aggregate(total=Sum('stockQuantity'))['total'] or 0

    # Produits en stock faible
    low_stock_products = products.filter(stockQuantity__lte=F('alertThreshold'))

    # Fournisseurs
    suppliers = Supplier.objects.all()

    # Mouvements aujourd'hui
    today = timezone.now().date()
    today_movements = Mouvement.objects.filter(dateMvt=today)

    # Derniers mouvements
    recent_movements = Mouvement.objects.order_by('-dateMvt')[:5]

    # Données pour graphique (7 derniers jours)
    dates = []
    entries = []
    exits = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        dates.append(day.strftime("%d/%m"))

        day_entries = Mouvement.objects.filter(
            dateMvt=day, type='entree'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        day_exits = Mouvement.objects.filter(
            dateMvt=day, type='sortie'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        entries.append(day_entries)
        exits.append(day_exits)

    #  Contexte
    context = {
        "totalStock": total_stock,
        "lowStockProducts": low_stock_products,
        "suppliers": suppliers,
        "todayMovements": today_movements,
        "recentMovements": recent_movements,

        # Pour Chart.js
        "dates": json.dumps(dates),
        "entries": json.dumps(entries),
        "exits": json.dumps(exits),
    }

    return render(request, "gestions/dashboard.html", context)