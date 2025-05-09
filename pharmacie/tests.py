from django.test import TestCase, Client
from django.urls import reverse
from .models import Pharmacie, Garde
from datetime import date, timedelta
from django.core import mail


class PharmacieGardeTests(TestCase):

    def setUp(self):
        self.pharmacie = Pharmacie.objects.create(
            Nom="Pharmacie du Centre",
            adresse="123 rue principale",
            ville="Antananarivo",
            telephone="0321234567",
            latitude=-18.8792,
            longitude=47.5079
        )

        self.garde = Garde.objects.create(
            pharmacie=self.pharmacie,
            debut_garde=date.today(),
            fin_garde=date.today() + timedelta(days=2)
        )

    def test_pharmacie_creation(self):
        self.assertEqual(Pharmacie.objects.count(), 1)
        self.assertEqual(self.pharmacie.ville, "Antananarivo")

    def test_garde_valide(self):
        self.assertEqual(Garde.objects.count(), 1)
        self.assertEqual(self.garde.pharmacie.Nom, "Pharmacie du Centre")

    def test_garde_chevauchement(self):
        garde2 = Garde(
            pharmacie=self.pharmacie,
            debut_garde=date.today() + timedelta(days=1),
            fin_garde=date.today() + timedelta(days=3)
        )
        with self.assertRaises(Exception):  # ValidationError
            garde2.clean()

    def test_vue_pharmacies_par_ville(self):
        response = self.client.get(reverse('pharmacies_par_ville', args=["Antananarivo"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pharmacie du Centre")

    def test_contact_form_envoi(self):
        response = self.client.post(reverse('contact'), {
            'nom': 'Jean',
            'email': 'jean@example.com',
            'message': 'Bonjour, ceci est un test.'
        }, follow=True)

        self.assertRedirects(response, reverse('accueil'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Bonjour, ceci est un test.", mail.outbox[0].body)



