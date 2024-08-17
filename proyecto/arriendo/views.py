from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,  authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileUpdateForm, PropertyForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Property, Commune, Region

# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect('/accounts/login')
            except Exception as e:
                print(f"Error al guardar el usuario: {e}") 
                messages.error(request, 'Hubo un error al registrar el usuario.')
        else:
            print(form.errors)  
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            try:
                profile_form.save()
                messages.success(request, 'Perfil guardado exitosamente')
                return redirect('/')  
            except Exception as e:
                print(f"Error al guardar el usuario: {e}") 
                messages.error(request, 'Hubo un error al guardar el usuario.')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        print(profile_form.errors)

    context = {
        "profile_form": profile_form
    }
    return render(request, 'profile.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            form.add_error(None, 'Email o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect

@login_required
def add_property(request):
    if request.user.user_type_id == 1:
        if request.method == 'POST':
            property_form = PropertyForm(request.POST)
            if property_form.is_valid():
                property = property_form.save(commit=False) 
                property.owner = request.user 
                property.save()
                return redirect('/')   
        else:
            property_form = PropertyForm()
        
        context = {
            "property_form": property_form
        }
        return render(request, 'publication.html', context )
    else:
        return redirect('/')
    
@login_required
def get_properties(request):
   
    properties = Property.objects.all()
    communes = Commune.objects.all()
    regions = Region.objects.all()

    context = {
        "properties": properties,
        "communes": communes,
        "regions": regions
    }
       
    if request.method == "POST":
        if "region" in request.POST:
            request_region = request.POST["region"]
            communes = Commune.objects.filter(region_id=request_region)
            properties = properties.filter(commune__region_id=request_region)
            context["communes"] = communes
            context["region_selected"] = request_region
            context["properties"] = properties
        if "commune" in request.POST:
            request_commune= request.POST["commune"]
            properties = properties.filter(commune_id=request_commune)
            context["commune_selected"] = request_commune
            context["properties"] = properties

    return render(request, 'properties.html', context)

@login_required
def get_property(request, id):
    property = get_object_or_404(Property, id=id)
    context = {
        "property": property
    }
    return render(request, 'property.html', context)

@login_required
def my_properties(request):
    owner = request.user
    print(owner)
    properties = Property.objects.filter(owner=owner)
    print(properties)
    context = {
        "properties": properties
    }
    return render(request, 'my-properties.html', context)

@login_required
def delete_property(request, id):
  
    property_instance = Property.objects.get(id=id)
    property_instance.delete()
    
    return redirect('my_properties') 

@login_required
def edit_property(request, id):
    property = Property.objects.get(id=id)
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, instance=property)
        if property_form.is_valid():
            property_form.save()
            return redirect('my_properties')
    else:
        property_form = PropertyForm(instance=property)

    context = {
        'property_form': property_form,
        'property': property
    }
    return render(request, 'edit_property.html', context)

 