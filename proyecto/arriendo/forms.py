from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from .models import User, UserType, Property, HouseType, Commune

class SignUpForm(UserCreationForm):
    rut = forms.CharField(min_length=8, max_length=9, required=True)
    email = forms.EmailField(required=True)
    second_name = forms.CharField(max_length=50, required=False)
    second_surname = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    user_type = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None
    )

    class Meta:
        model = User
        fields = (
            'rut', 'first_name', 'second_name', 'last_name', 'email', 
            'second_surname', 'address', 'phone_number', 'user_type', 
            'password1', 'password2'
        )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['user_type'].initial = self.instance.user_type


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    second_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=True)
    second_surname = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    user_type = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'second_name', 'last_name', 'email',
            'second_surname', 'address', 'phone_number', 'user_type'
        )

class PropertyForm(forms.ModelForm):
    house_type = forms.ModelChoiceField(
        queryset = HouseType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    commune = forms.ModelChoiceField(
        queryset = Commune.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Property
        fields =  (
            'name', 'description', 'constructed_meters', 'total_meters', 'parking_lots', 'rooms', 'bathrooms', 'address', 'commune', 'price', 'house_type', 'image_url'
        )