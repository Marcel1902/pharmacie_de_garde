
from django.contrib import admin
from django.urls import path, include
from pharmacie import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.page_principale, name="accueil"),
    path('api/pharmacies/<str:ville>/', views.pharmacies_par_ville, name='pharmacies_par_ville'),
    path('contact', views.contact, name="contact"),
]
