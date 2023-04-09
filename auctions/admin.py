from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "categoria")
    # con list... podes ver todas las opciones costumizables que hay.

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "fecha", "listing", "usuario")

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "imagen", "descripcion", "precio", "dueño", "Activo", "categoria")


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Comment, CommentAdmin)


# enves de poner admin.site... podes registrar un model con un decorador, ejemplo:
# @admin.register(AuctionListing)
# y aca podes poner la customización que quieras

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display= ("usuario", "fecha", "bid", "listing")

@admin.register(watchlist)
class watchlistAdmin(admin.ModelAdmin):
    list_display= ("usuario", "listing")

# admin.site.register(Oferta)
