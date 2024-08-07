import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from arriendo.models import Property, Commune

ruta_archivo = os.path.join("hito-2", "properties_by_communes.txt")

def properties_by_commune():
    communes = Commune.objects.all()
    
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        for commune in communes:
            properties = Property.objects.filter(
                commune=commune,
                active=True
            ).filter(
                name__contains=commune.name
            ).filter(
                description__contains=commune.name
            ).values('name', 'description')
            
            if properties.exists():  
                file.write(f'Comuna: {commune.name}\n')
                for prop in properties:
                    file.write(f'Nombre: {prop["name"]}\n')
                    file.write(f'Descripción: {prop["description"]}\n')
                    file.write('---\n')
                file.write('\n')  

if __name__ == "__main__":
    properties_by_commune()
