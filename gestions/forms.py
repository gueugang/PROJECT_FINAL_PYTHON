from django import forms
from .models import Administrateur, Supplier, Product, Category, Fournir, Mouvement

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

TAILWIND_INPUT_CLASS = 'w-2xl px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'

# class AdminForm(forms.ModelForm):
#     class Meta:
#         model = Administrateur
#         fields = ['name', 'email', 'username', 'password']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder':'choisir le projet', 'class':TAILWIND_INPUT_CLASS}),
#             'email': forms.EmailInput(attrs={'placeholder':'exemple@gmail.com', 'class': TAILWIND_INPUT_CLASS}),
#             'username' : forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
#             'pasword': forms.PasswordInput(attrs ={'class': TAILWIND_INPUT_CLASS}),            'pasword': forms.PasswordInput(attrs ={'class': TAILWIND_INPUT_CLASS}),
#         }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'adress', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'choisir le projet', 'class':TAILWIND_INPUT_CLASS}),
            'adress': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'phone': forms.TextInput(attrs={'class':TAILWIND_INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'placeholder':'exemple@gmail.com', 'class': TAILWIND_INPUT_CLASS}),
            
        }
        
# class MagasinierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ['name', 'adress', 'phone', 'email']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder':'choisir le projet', 'class':TAILWIND_INPUT_CLASS}),
#             'adress': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
#             'phone': forms.TextInput(attrs={'class':TAILWIND_INPUT_CLASS}),
#             'email': forms.EmailInput(attrs={'placeholder':'exemple@gmail.com', 'class': TAILWIND_INPUT_CLASS}),
#             'username' : forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
#             'pasword': forms.PasswordInput(attrs ={'class': TAILWIND_INPUT_CLASS}),
#         }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description','unitPrice', 'stockQuantity', 'alertThreshold','image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'description': forms.Textarea(attrs={ 'class': TAILWIND_INPUT_CLASS}),
            'unitPrice' : forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'stockQuantity': forms.NumberInput(attrs ={'class': TAILWIND_INPUT_CLASS}),
            'alertThreshold': forms.NumberInput(attrs ={'class': TAILWIND_INPUT_CLASS}),
            'category': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['nameCategory', 'description']
        widgets = {
            'nameCategory': forms.TextInput(attrs={'class':TAILWIND_INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class':TAILWIND_INPUT_CLASS}),
        }
        
 
 
# formulaire pour la creation des utilisateur

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    adress = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    role = forms.ChoiceField(
        choices=[("Magasinier","Magasinier"), ("Administrateur","Administrateur")],
        widget=forms.Select(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": TAILWIND_INPUT_CLASS
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "name", "adress", "role"]
# class UserRegisterForm(UserCreationForm):
#     name = forms.CharField(max_length=20)
#     email = forms.EmailField()
#     adress = forms.CharField(max_length=25)
#     role = forms.ChoiceField(choices=[("Magasinier","Magasinier"), ("Administrateur","Administrateur")])

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2", "name", "adress", "role"]
    
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        })
    )
    
class FournirForm(forms.ModelForm):
    class Meta:
        model = Fournir
        fields = ['product', 'supplier', 'unitPrice']
        widgets = {
            'product': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
            'supplier': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
            'unitPrice': forms.TextInput(attrs={'class':TAILWIND_INPUT_CLASS}),
        }
        
class MouvementForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['product', 'dateMvt', 'quantity', 'valide', 'type', 'magasinier', 'administrateur']
        widgets ={
            'product': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
            'dateMvt': forms.DateInput(attrs={'class':TAILWIND_INPUT_CLASS}),
            'quantity': forms.TextInput(attrs={'class':TAILWIND_INPUT_CLASS}),
            'valide': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'type': forms.Select(attrs={'class': TAILWIND_INPUT_CLASS}),
            'magasinier': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
            'administrateur': forms.Select(attrs={'class':TAILWIND_INPUT_CLASS}),
        }