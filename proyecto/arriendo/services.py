from .models import User, UserType, HouseType, Region, Commune, Property, Status, Contract
from django.utils.crypto import get_random_string

def create_user_type(name):
    try:
        type = UserType(name=name)
        type.save()
        return type
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_user(rut, first_name, second_name, last_name, second_surname, address, phone_number, email, user_type, password):
    try:
        type = UserType.objects.get(id=user_type)
        username = rut + get_random_string(4)
        new_user = User(rut=rut, first_name=first_name, second_name=second_name, last_name=last_name, second_surname=second_surname, address=address, phone_number=phone_number, email=email, user_type=type, username=username, password=password)
        new_user.set_password(password) 
        new_user.save()
        return new_user
    except UserType.DoesNotExist:
        print(f"Error: Tipo de usuario no encontrado con ID: {user_type}")
        return None
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        return None

def create_house_type(name):
    try:
        type = HouseType(name=name)
        type.save()
        return type
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_region(name):
    try:
        region = Region(name=name)
        region.save()
        return {'id': region.id, 'name': region.name}
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def add_commune(name, region_id):
    try:
        region = Region(id=region_id)
        commune = Commune(name=name, region_id=region)
        commune.save()
        return {'id': commune.id, 'name': commune.name}
    except Exception as e:
        print(f"Error: {e}")

def create_property(name,description, constructed_meters, total_meters, parking_lots, rooms, bathrooms, address, commune, house_type, price, rut, tenant_rut=None):
    try:
        owner = User.objects.get(rut=rut)
        type = HouseType.objects.get(id=house_type)
        commune = Commune.objects.get(id=commune)
        tenant = None
        if tenant_rut:
            try:
                tenant = User.objects.get(rut=tenant_rut)
            except User.DoesNotExist:
                print(f"Usuario {tenant_rut} no encontrado.")
        new_property = Property(name=name, description=description, constructed_meters=constructed_meters, total_meters=total_meters, parking_lots=parking_lots, rooms=rooms, bathrooms=bathrooms, address=address, commune=commune, house_type=type, price=price, owner=owner, tenant=tenant)
        new_property.save()
        return new_property
    except HouseType.DoesNotExist:
        print(f"Error: Tipo de propiedad no encontrada")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_property(id):
    try:
        property= Property.objects.get(id=id)
        return property
    except Property.DoesNotExist:
        print(f"Propiedad con ID {id} no encontrada.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_property(id, name, description, constructed_meters, total_meters, parking_lots, rooms, bathrooms, address, commune, house_type, price):
    try:
        type = HouseType(id=house_type)
        property= Property.objects.get(id=id)
        commune = Commune.objects.get(id=commune)
        property.name = name
        property.description = description
        property.constructed_meters = constructed_meters
        property.total_meters = total_meters
        property.parking_lots = parking_lots
        property.rooms = rooms
        property.bathrooms = bathrooms
        property.address = address
        property.commune = commune
        property.house_type = type
        property.price = price
        property.save()
    except Property.DoesNotExist:
        print("Propiedad no encontrada.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def delete_property(id):
    try:
        property = Property.objects.get(id=id)
        property.delete()
        return True
    except Property.DoesNotExist:
        print("Propiedad no encontrada.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def create_status(name):
    try:
        type = Status(name=name)
        type.save()
        return type
    except Exception as e:
        print(f"Error: {e}")
        return None

def request_property(property, tenant, status):
    try:
        property = Property.objects.get(id=property)
        tenant = User.objects.get(rut=tenant)
        status = Status.objects.get(name=status)
        contract = Contract(property=property,tenant=tenant,status=status)
        contract.save()
        return contract
    except Property.DoesNotExist:
        print("Propiedad no encontrada")
        return None
    except User.DoesNotExist:
        print("Error Arrendatario no encontrado")
        return None
    except Status.DoesNotExist:
        print(f"Estado no encontrado")
        return None
    except Exception as e:
        print(f"Error al solicitar la propiedad: {e}")
        return None


def update_status(contract, new_status):
    try:
        contract = Contract.objects.get(id=contract)
        property = contract.property
        new_status = Status.objects.get(name=new_status)
        if new_status == "aceptado":
            contract.status = new_status
            property.active = False
            property.save()
        contract.status = new_status
        contract.save()
        return contract
    except Contract.DoesNotExist:
        print(f"Error: Contrato no encontrado.")
        return None
    except Status.DoesNotExist:
        print(f"Estado no encontrado.")
        return None
    except Exception as e:
        print(f"Error al actualizar el estado del contrato: {e}")
        return None
