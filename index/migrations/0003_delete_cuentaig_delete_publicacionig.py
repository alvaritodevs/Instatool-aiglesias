# Generated by Django 4.2 on 2023-05-20 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_cuentaig_publicacionig_delete_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CuentaIg',
        ),
        migrations.DeleteModel(
            name='PublicacionIg',
        ),
    ]