# Generated by Django 4.1.3 on 2023-03-03 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_rename_valor_inicial_auctionlisting_valor"),
    ]

    operations = [
        migrations.RenameField(
            model_name="auctionlisting",
            old_name="valor",
            new_name="precio",
        ),
    ]