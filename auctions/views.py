from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from .forms import *

from .models import *





categorias_form = CategoriasForm()

def index(request):
    productos = AuctionListing.objects.all()
    # aca accedes a los fields de CategoriasForm y le pones que el formulario categorias su label sea igual a filtrar por.
    categorias_form.fields["categorias"].label = "Filter by:"
    categorias_form.fields["categorias"].empty_label = 'All the products'
    return render(request, "auctions/index.html", {"productos": productos, "categorias": categorias_form})

def login_view(request):
    print(request.META.get('HTTP_REFERER'))
    # esto tiene separado lo que te muestra y lo que va a pasar si tocas el post.
    if request.META.get('HTTP_REFERER') != "http://127.0.0.1:8000/login":
        preview_page = request.META.get('HTTP_REFERER')
        print(preview_page)
    
    # preview_page = '/'.join(preview_page.split('/')[-2:])
    
    
    
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        

        # Check if authentication successful
        if user is not None:
            login(request, user)
            #preview_page = '/'.join(preview_page.split('/')[-2:])
            # preview_page = '/'.join(preview_page.split('/')[-1:])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        elif username == "":
            return render(request, "auctions/register.html", {
                "message": "You haven't insert a valid username."
            })

            

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def new_listing(request):
    if request.method == "POST":
        formulario = CreateListingF(request.POST)
        categorias_value = CategoriasForm(request.POST)
        if categorias_value.is_valid() and formulario.is_valid():

            producto = formulario.cleaned_data["producto"].title()
            descripcion = formulario.cleaned_data["descripcion"].title()
            imagen = formulario.cleaned_data["imagen"]
            imagen2 = formulario.cleaned_data["imagen2"]
            imagen3 = formulario.cleaned_data["imagen3"]
            precio = formulario.cleaned_data["precio"]
            dueño = request.user
        
            new_listing = AuctionListing(
                producto = producto,
                descripcion = descripcion,
                imagen = imagen,
                imagen2= imagen2,
                imagen3= imagen3,
                precio = precio,
                dueño = dueño,
                
            )

            try:
                categorias_value = categorias_value.cleaned_data['categorias']
            except:
                categorias_value = None
            
            new_listing.categoria = categorias_value
                

            #TODO tambien podias hacer asi:
            # new_listing = AuctionListing()
            # new_listing.producto = formulario.cleaned_data["producto"]
            # new_listing.descripcion = formulario.cleaned_data["descripcion"]
            # new_listing.imagen = formulario.cleaned_data["imagen"]
            # new_listing.precio = formulario.cleaned_data["precio"]
            # new_listing.Activo = formulario.cleaned_data["Activo"]
            # new_listing.dueño = request.user


            if producto == "":
                return render(request, "auctions/new_listing.html", {
                    "message": "You did not provide a valid name for your product", "Formularios": CreateListingF(), "categorias":  CategoriasForm(),
                })
            else:
                new_listing.save()
                #TODO enves de poner .save() tambien podes poner new_listing = AuctionListing.objets.create (datos)

                return redirect("index")
        
        
    else:
        return render (request, "auctions/new_listing.html", {"Formularios": CreateListingF(), "categorias":  CategoriasForm(),})


def listing(request, id,):
    producto =  AuctionListing.objects.get(id=id)
    ofertaForm = FormOferta()
    
    ofertaForm.fields['oferta'].initial = (producto.precio)+100
    # oferta.fields['oferta'].min_value = (producto.precio)+100 no nos funcionó.
    comentarios = Comment.objects.filter(listing = producto.id)

    usuario = request.user
    last_bid = Bid.objects.filter(listing=producto).last() 
    # con el metodo last te devuelve la ultima bid que te aparece en el django admin.

    disabled = ""
    outline = "outline-"
    
    try:
        is_in_watchlist= watchlist.objects.filter(listing = producto.id, usuario = request.user)
        if is_in_watchlist:
            is_in_watchlist = True
        else:
            is_in_watchlist = False
    except:
        is_in_watchlist = False
        disabled = "disabled"
        outline = ""

    if request.method == "POST":
        oferta = FormOferta(request.POST)
        if oferta.is_valid() and oferta.cleaned_data['oferta'] >= producto.precio + 100:
            oferta = oferta.cleaned_data['oferta']



            Bid.objects.create(
                usuario = request.user,
                listing = producto,
                bid = oferta
            )
            # AuctionListing.precio = oferta no es necesario porque en models ya lo pudiste en la def save() es mejor trabajar con los modelos.


            return HttpResponseRedirect(reverse("listing", args= [id]))
        
        else:
            return render(request, "auctions/listing.html", {"producto": producto, "oferta":ofertaForm, "commentform": CommentsForm(), "comentarios": comentarios, "usuario": usuario,"last_bid": last_bid, "is_in_watchlist": is_in_watchlist, "disabled": disabled,"outline": outline, "message": f"Your bid must be greater than ${producto.precio}"})


    else:
        return render(request, "auctions/listing.html", {"producto": producto, "oferta": ofertaForm, "commentform": CommentsForm(), "comentarios": comentarios, "usuario": usuario, "last_bid": last_bid, "is_in_watchlist": is_in_watchlist, "disabled": disabled, "outline": outline})



def categoryFilter(request):
    # !cuando usas el metodo post y llamas al formulario lo que te devuelve es un diccionario.
    #podes poner print(request.POST["categorias"]) y en la terminal te va a salir
    if request.method == "POST":
        categorias_value = CategoriasForm(request.POST)
        if categorias_value.is_valid():
            categorias_value = categorias_value.cleaned_data['categorias']
            if categorias_value == None:
                return HttpResponseRedirect(reverse("index"))
                

            else:
                categorias_form.fields["categorias"].empty_label = 'All the products'
                productos = AuctionListing.objects.filter(Activo=True, categoria=categorias_value)
                return render(request, "auctions/index.html", {"productos": productos, "categorias": categorias_form})

import datetime
from django.utils import timezone

def post_comment(request, producto_id):
    if request.method == "POST":
        comentario = CommentsForm(request.POST)
        if comentario.is_valid():
            comentario = comentario.cleaned_data['message']
            
            Comment.objects.create(
                usuario = request.user,
                listing = AuctionListing.objects.get(id=producto_id),
                message = comentario,
                )
            return redirect("listing", id = producto_id)
        else:
            return render(request, "auctions/error.html", {"error": "error not valid form"})


def watchList(request, producto_id):
    if request.method == "POST":
        is_in_watchlist= watchlist.objects.filter(listing = producto_id, usuario = request.user)
        if is_in_watchlist:
            # entra a este if si no esta vacia la variable.
            # remove:
            is_in_watchlist.delete()
        else:
            # add:
            watchlist.objects.create(
                    usuario = request.user,
                    listing = AuctionListing.objects.get(id=producto_id),
                    )

        return redirect("listing", id = producto_id)



def watch_list_see(request):
    watchlist_user= watchlist.objects.filter(usuario = request.user)
    if not watchlist_user:
        watchlist_user = None
    # querysets = []
    # contador = 0
    # for queryset in watchlist_user:
    #     last_bid_user = Bid.objects.filter(listing=queryset.listing).last().usuario
    #     if last_bid_user == request.user:
    #         querysets.append(True)
    #     else:
    #         querysets.append(False)
    # no pudimos hacer esto porque no sabemos como reflejarlo en el template. 
    # productos = AuctionListing.objects.filter(listing = watchlist_user)

    return render(request, "auctions/watchlist.html",{"watchlist_user" : watchlist_user,})


def bid(request, producto_id):
    if request.method == "POST":
        producto =  AuctionListing.objects.get(id=producto_id)
        oferta = FormOferta(request.POST)
        if oferta.is_valid() and oferta.cleaned_data['oferta'] >= producto.precio:
            oferta = oferta.cleaned_data['oferta']

            Bid.objects.create(
                usuario = request.user,
                listing = producto,
                bid = oferta
            )

            # AuctionListing.precio = oferta no es necesario porque en models ya lo pudiste en la def save()
            
            return redirect("listing", id = producto_id)

        else:
            return render(request, "auctions/listing.html", {"error": "La oferta que realizaste no es correcta"})

    
def closeListing(request, producto_id):
    if request.method == "POST":
        producto =  get_object_or_404(AuctionListing, id=producto_id)
        producto.Activo = False
        producto.save()
        return redirect("listing", id = producto_id)
