# admin_web_app/management/commands/create_test_computers.py
from django.core.management.base import BaseCommand
import random
from faker import Faker
from admin_web_app.models import Computer

class Command(BaseCommand):
    help = 'Create 10 test computers'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Limpiar la base de datos de ordenadores de prueba existentes (opcional)
        Computer.objects.filter(name__startswith='PC-Test-').delete()

        for i in range(1, 11):
            name = f"PC-Test-{i}"
            state = random.choice(['on', 'off'])
            icon = 'computer.png' if state == 'on' else 'computer-off.png'
            mac = fake.mac_address()
            ip = fake.ipv4(network='10.209.3.0/24')

            computer = Computer(name=name, state=state, icon=icon, mac=mac, ip=ip)
            computer.save()

        self.stdout.write(self.style.SUCCESS("10 test computers created successfully."))
