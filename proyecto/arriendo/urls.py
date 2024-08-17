from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

#URLS APP

urlpatterns = [
    path('', views.home),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile),
    path('signup', views.signup),
    path('publication', views.add_property),
    path('properties', views.get_properties, name='get_properties'),
    path('properties/<int:id>', views.get_property, name='property_detail'),
    path('my-properties', views.my_properties, name='my_properties'),
    path('properties/delete/<int:id>', views.delete_property, name='delete_property'),
    path('properties/edit/<int:id>', views.edit_property, name='edit_property')
]