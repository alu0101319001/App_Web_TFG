# admin_web_app/models.py
from django.db import models

class Computer(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='img/', blank=True, null=True)  # Imagen del estado
    mac = models.CharField(max_length=17, blank=True, null=True, unique=True)  # Dirección MAC como único
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=True, null=True)  # Dirección IP
    warning = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_by_name_and_mac(cls, name, mac, defaults=None):
        """
        Obtener o crear un objeto Computer basado en el nombre y la MAC.
        Si ya existe un objeto con el mismo nombre y MAC, devuelve el objeto existente.
        Si no existe, crea un nuevo objeto con los datos proporcionados.
        """
        defaults = defaults or {}
        obj, created = cls.objects.get_or_create(name=name, mac=mac, defaults=defaults)
        
        if not created:
            # Si el objeto ya existía, mantener el valor actual de 'warning' si no está presente en defaults
            if 'warning' not in defaults:
                defaults['warning'] = obj.warning  # Mantener el valor actual de 'warning'

            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()

        return obj
