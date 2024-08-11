from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

#URLS APP

urlpatterns = [
    path('', views.home),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile),
    path('signup', views.signup)
]