# Generated by Django 4.1.7 on 2023-05-24 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuentaig',
            old_name='ispass',
            new_name='igpass',
        ),
    ]