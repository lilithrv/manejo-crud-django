from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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
            return redirect('home')  
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