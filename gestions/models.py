

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    nameCategory = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nameCategory

class Magasinier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    adress = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    adress = models.CharField(max_length=25)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    name= models.CharField(max_length=50)
    adress = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name
    

    
     
class Product(models.Model):
    
    name = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    unitPrice = models.FloatField(null=True, blank=True )
    stockQuantity = models.IntegerField()
    alertThreshold = models.IntegerField()
    image = models.ImageField(upload_to="gestions/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="gestions", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Mouvement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="mouvements")
    dateMvt = models.DateField()
    quantity = models.IntegerField()
    valide = models.BooleanField()
    type = models.CharField(max_length=10, choices=[
    ('entree', 'Entrée'),
    ('sortie', 'Sortie'),])
    magasinier = models.ForeignKey(Magasinier, on_delete= models.CASCADE, related_name="enregistreMvt", null=True, blank=True)
    administrateur = models.ForeignKey(Administrateur, on_delete=models.CASCADE, related_name="gestion",null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def appliquer_mouvement(self):

        product = self.product

        if self.type == 'entree':
            product.stockQuantity += self.quantity

        elif self.type == 'sortie':

            if product.stockQuantity < self.quantity:
                raise ValueError("Stock insuffisant")

            product.stockQuantity -= self.quantity

        product.save()
    def save(self, *args, **kwargs):

                # vérifier si c'est un ancien mouvement
        if self.pk:
            ancien = Mouvement.objects.get(pk=self.pk)

            # si il devient valide
            if not ancien.valide and self.valide:
                self.appliquer_mouvement()

        else:
            # nouveau mouvement
            if self.valide:
                self.appliquer_mouvement()

        super().save(*args, **kwargs)
    
    


class Alert(models.Model):
    message = models.CharField(max_length=200)
    dateAlert = models.DateField()
    status = models.CharField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Alerts")  
    
class Fournir(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="fournir") 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="fournir")
    unitPrice = models.FloatField()
    

    
 
    