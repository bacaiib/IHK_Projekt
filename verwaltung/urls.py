from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views, admin
from .auth_views import CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-success/', views.logout_success, name='logout_success'),  # Neue URL
    path('kunden/', views.kunden_uebersicht, name='kunden-uebersicht'),
    path('kunde/<int:kunden_nr>/', views.kunden_detail, name='kunden_detail'),
    path('kunde/neu/', views.kunde_neu, name='kunde-neu'),
    path('kunden/<int:pk>/edit/', views.kunde_edit, name='kunde-edit'),
    path('vermerk/erfassen/', views.vermerk_erfassen, name='vermerk-erfassen'),
    path('kunde/data/<int:kunden_nr>/', views.get_kunde_data, name='get-kunde-data'),
    path('vermerk/', views.vermerk_uebersicht, name='vermerk-uebersicht'),
    path('vermerk/<int:gespraechs_id>/', views.vermerk_detail, name='vermerk_detail'),
    path('vermerk/<int:pk>/edit/', views.vermerk_edit, name='vermerk-edit'),
    path('kunde/<int:kunden_nr>/loeschen/', views.kunde_loeschen, name='kunde-loeschen'),
    path('vermerk/<int:gespraechs_id>/loeschen/', views.vermerk_loeschen, name='vermerk-loeschen')
]