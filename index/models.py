from django.db import models


class PublicacionIg(models.Model):

  username = models.CharField(max_length=255)
  piefoto = models.CharField(max_length=255)
  fecha = models.CharField(max_length=255)
  imagen = models.CharField(max_length=255)


class CuentaIg(models.Model):
  
  username = models.CharField(max_length=255)
  iguser = models.CharField(max_length=255)
  igpass = models.CharField(max_length=255)

  def __str__(self):
        return self.username
  



  