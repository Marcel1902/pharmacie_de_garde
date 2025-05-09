from django.db import models
from django.core.exceptions import ValidationError

class Pharmacie(models.Model):
    Nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    ville = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    latitude = models.FloatField(default=0.0000)
    longitude = models.FloatField(default=0.0000)

    def __str__(self):
        return self.Nom

class Garde(models.Model):
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE)
    debut_garde = models.DateField()
    fin_garde = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pharmacie.Nom} (du {self.debut_garde.strftime('%d/%m/%Y')} au {self.fin_garde.strftime('%d/%m/%Y')})"


    def clean(self):
        super().clean()
        if self.fin_garde < self.debut_garde:
            raise ValidationError("La date de fin doit être après la date de début.")
        
        # Vérifie le chevauchement
        chevauchement = Garde.objects.filter(
            pharmacie=self.pharmacie,
            debut_garde__lte=self.fin_garde,
            fin_garde__gte=self.debut_garde
        ).exclude(id=self.id)

        if chevauchement.exists():
            raise ValidationError("Cette pharmacie a déjà une garde durant cette période.")

