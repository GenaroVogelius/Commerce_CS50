from .models import *

from django import forms



class CategoriasForm(forms.Form):
    # choices = [(categoria.id, str(categoria)) for categoria in Category.objects.all()]
    # categorias = forms.ChoiceField(choices= choices[::-1], required=False,)
    # esto es una list comphrension para hacer un bucle for de las categorias que existen.
    # choices = ( tupla ) son los valores que deben ir ahi. the first element should be the value of the option, and the second element should be the text that will be displayed to the user.
    categorias = forms.ModelChoiceField(
        label="", 
        queryset=Category.objects.all(), 
        required=False, 
        empty_label="Without declaring",
        widget=forms.Select(attrs={
            "class": "form-select",
            "aria-label": "Floating label select example",
            "id": "categoriasForm",

            })
            )


class CreateListingF(forms.Form):
    producto = forms.CharField(
        max_length=65,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write the name of the product here",
                "id": "productoForm",
            }
        ),
    )
    

    descripcion = forms.CharField(
        max_length=350,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write a short description of the product here",
                "id": "descriptionForm",
            }
        ),
    )

    
    imagen = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Insert a URL of your product image here",
                "id": "imageForm",
            }
        ),
    )
    imagen2 = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Insert a URL of your product image here",
                "id": "imageForm",
            }
        ),
    )
    imagen3 = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Insert a URL of your product image here",
                "id": "imageForm",
            }
        ),
    )

    precio = forms.IntegerField(
        min_value=100.1,
        label="Starter price",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "aria-label": "Amount (to the nearest dollar)",
            "placeholder": "Starter price"})
            )


class FormOferta(forms.Form):
        oferta = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "aria-label": "Amount (to the nearest dollar)",

            "placeholder": "precio"}),
            )

class CommentsForm(forms.Form):
    message = forms.CharField(max_length=100, 
            required=False, 
            label="",
            widget= forms.Textarea(attrs={
            "class": "form-control",
            "style":"height: 100px",
            "placeholder": "precio"})
    )


