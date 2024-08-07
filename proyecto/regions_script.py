import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from arriendo.models import Property

ruta_archivo = os.path.join("hito-2", "properties_by_region.txt")

def properties_by_region():
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        properties = Property.objects.filter(active=True).select_related('commune')

        regions = {}
        for property in properties:
            region = property.commune.region_id
            if region not in regions:
                regions[region] = []
            regions[region].append(property)

        for region, properties in regions.items():
            file.write(f'Región: {region.name}\n')
            if properties:
                file.write('Inmuebles:\n')
                for property in properties:
                    file.write(f'''
                    Nombre: {property.name}
                    Descripción: {property.description}
                    M2 construidos: {property.constructed_meters}
                    M2 totales: {property.total_meters}
                    N° Habitaciones: {property.rooms}
                    N° Estacionamiento: {property.parking_lots}
                    N° baño: {property.bathrooms}
                    Dirección: {property.address}
                    Comuna: {property.commune.name}
                    Tipo de vivienda: {property.house_type}
                    Precio: {property.price}
                    Dueño: {property.owner.first_name} {property.owner.last_name}
                    -------------------------
                    ''')
            file.write('\n')

if __name__ == "__main__":
    properties_by_region()
