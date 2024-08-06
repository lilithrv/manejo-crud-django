from django.db import models
from .validate import validate_rut
from django.core.exceptions import ValidationError

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class UserType(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
 
    rut = models.CharField(max_length=9, primary_key=True)
    second_name = models.CharField(max_length=50, blank=True)
    second_surname= models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)
    phone_number= models.CharField(max_length=15, null=False)
    user_type= models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='users')
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def clean(self):
        super().clean()
        if not validate_rut(self.rut):
            raise ValidationError({'El RUT ingresado no es válido.'})

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return(f'''
        Rut: {self.rut}
        Nombres: {self.first_name} {self.second_name}
        Apellidos: {self.last_name} {self.second_surname}
        Direccion: {self.address}
        Telefono: {self.phone_number}
        Email: {self.email}
        Tipo de usuario: {self.user_type}
        ''')
    
class HouseType(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50, null=False)

class Commune(models.Model):
    name = models.CharField(max_length=50, null=False)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='communes')

class Property(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=1000, null=False)
    constructed_meters = models.FloatField(null=False)
    total_meters = models.FloatField()
    parking_lots = models.IntegerField(null=False)
    rooms = models.IntegerField(null=False)
    bathrooms = models.IntegerField(null=False)
    address = models.CharField(max_length=50, null=False)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='commune_properties')
    price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    house_type = models.ForeignKey(HouseType, on_delete=models.CASCADE, related_name='properties')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    tenant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='rented_properties')
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return(f'''
        Nombre: {self.name}
        Descripción: {self.description}
        M2 construidos: {self.constructed_meters}
        M2 totales: {self.total_meters}
        N° Habitaciones: {self.rooms}
        N° Estacionamiento: {self.parking_lots}
        N° baño: {self.bathrooms}
        Dirección: {self.address}
        Comuna: {self.commune}
        Tipo de vivienda: {self.house_type}
        Precio: {self.price}
        Dueño: {self.owner.first_name} {self.owner.last_name}
        ''')

class Status(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name


class Contract(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contracts')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='contracts')

    def __str__(self):
        return(f'''
        Propiedad: {self.property.name}
        Estado propiedad: {self.status}
        Arrendatario: {self.tenant.first_name} {self.tenant.last_name}
        ''')
