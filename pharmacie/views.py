from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Pharmacie, Garde
from datetime import datetime
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.

def pharmacies_par_ville(request, ville):
    gardes = Garde.objects.filter(pharmacie__ville=ville)
    data = [
        {
            "nom": garde.pharmacie.Nom,
            "adresse": garde.pharmacie.adresse,
            "telephone": garde.pharmacie.telephone,
            "latitude": garde.pharmacie.latitude,
            "longitude": garde.pharmacie.longitude,
            "periode": f"{garde.debut_garde.strftime('%d/%m/%Y')} - {garde.fin_garde.strftime('%d/%m/%Y')}"

        }
        for garde in gardes
    ]
    return JsonResponse(data, safe=False)



def page_principale(request):
    villes = Pharmacie.objects.values_list('ville', flat=True).distinct()
    return render(request, 'pharmacie/index.html', {'villes': villes, "now": datetime.now()})


def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if nom and email and message:
            sujet = f"Nouveau message de {nom}"
            corps = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                sujet,
                corps,
                email,  # expéditeur
                ['faniloniainatanguymarcel@gmail.com'],  # destinataire
                fail_silently=False,
            )
            
            messages.success(request, "Votre message a été envoyé avec succès.")
            return redirect('accueil')

        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'pharmacie/index.html')