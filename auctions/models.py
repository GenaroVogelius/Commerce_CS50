from django.contrib.auth.models import AbstractUser
from django.db import models


from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass


from django.utils import timezone


class Category(models.Model):
    categoria = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.categoria

# class Precio(models.Model):
#     oferta = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100), MaxValueValidator(9999999999)])

# class Bid(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_bid")
#     fecha = models.DateField(auto_now_add=True)
#     bid = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100), MaxValueValidator(9999999999)])
#     producto = models.CharField(max_length=65, )

#     def __str__(self):
#         return str(self.bid)
    

class AuctionListing(models.Model):
    producto = models.CharField(max_length=65)
    imagen = models.CharField(max_length=1000, blank=True, null=True)
    imagen2 = models.CharField(max_length=1000, blank=True, null=True)
    imagen3 = models.CharField(max_length=1000, blank=True, null=True)
    descripcion = models.CharField(max_length=350)
    precio = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(9999999999)])
    Activo = models.BooleanField(default=True)
    dueño = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user")
    categoria = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name = "category")
    # el related_name no puede tener el mismo nombre que el atributo de la clase a la cual llama. por eso pusiste category y no categoria.
    

    def __str__(self):
        return self.producto

    def save(self, *args, **kwargs):
        self.producto = self.producto.title()
        super(AuctionListing, self).save(*args, **kwargs)
    #TODO el def save lo que hace es que cuando se guarde el producto name, se le aplique el metodo title().


class Comment(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comment_user")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "comment_listing")
    message = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.message}"
    



class Bid(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_bid")
    fecha = models.DateField(auto_now_add=True)
    bid = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(9999999999)])
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "listing_bid")

    def __str__(self):
        return str(self.bid)
    
    def clean(self):
        if self.bid is not None and self.bid < self.listing.precio and self.bid < self.bid:
            raise ValidationError(f"Bid must be greater than {self.listing.precio}.")
    #TODO hiciste esta def de clean para que el field bid no pueda ser menor al precio que esta contenido en listing

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.precio = self.bid
        self.listing.save()
        
    #TODO el def save lo que hace es que cuando guardes la bid esta pase a ser el precio actual del producto en listings.


class watchlist(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "listing_watchlist")

    
