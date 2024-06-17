# admin_web_app/models.py
from django.db import models

class Computer(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    icon =  models.ImageField(upload_to='img/', blank=True, null=True)  # Imagen del estado
    mac = models.CharField(max_length=17, blank=True, null=True)  # Dirección MAC
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=True, null=True)  # Dirección IP
    warning = models.BooleanField(default=False)

    def __str__(self):
        return self.name
