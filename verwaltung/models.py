from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Kunde(models.Model):
    kunden_nr = models.AutoField(primary_key=True)
    firma = models.CharField(max_length=60)
    anschrift = models.CharField(max_length=60)
    plz = models.CharField(max_length=10, blank=True)
    stadt = models.CharField(max_length=50)
    telefon_nr = models.CharField(max_length=20, blank=True)
    fax_nr = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.firma} ({self.kunden_nr})"

class Vermerk(models.Model):
    gespraechs_id = models.AutoField(primary_key=True) # Automatisch generierte ID als Primärschlüssel
    datum = models.DateField(auto_now_add=True)  # Datum wird beim Erstellen automatisch gesetzt
    uhrzeit = models.TimeField() # Uhrzeit des Gesprächs (automatisch über save())

    kontaktart = models.CharField( # Auswahlfeld für Art des Kontakts
        max_length=18,
        choices=[('Eingehender Anruf', 'Anruf von'),
                 ('Ausgehender Anruf', 'Anruf bei'),
                 ('Im Büro', 'Besuch von'),
                 ('Beim Kunden', 'Besuch bei')],
        default='Anruf'
    )
    anrede = models.CharField( # Auswahlfeld für Anrede
        max_length=10,
        choices=[('Herr', 'Herr'), ('Frau', 'Frau'), ('Divers', 'Divers')],
        default='Herr'
    )
    name = models.CharField(max_length=30)
    betreff = models.CharField(max_length=40)
    wunsch = models.CharField(
        max_length=20,
        choices=[('wünscht Rückruf', 'wünscht Rückruf'), ('wünscht Termin', 'wünscht Termin'),
                 ('ruft wieder zurück', 'ruft wieder an')],
        default='wünscht Rückruf'
    )
    gespraechsinhalt = models.TextField()
    firmen_id = models.ForeignKey(Kunde, on_delete=models.CASCADE, related_name='vermerke') # Fremdschlüssel zum Kunden
    aufgenommen = models.CharField(max_length=40, default='')  # Mitarbeiter, der das Gespräch aufgenommen hat
    verfuegung = models.CharField(max_length=100, default='')  # Interne Weiterleitung oder Folgeaktion

    def save(self, *args, **kwargs):
        if not self.pk:
            from django.utils import timezone
            self.uhrzeit = timezone.localtime(timezone.now()).time().replace(second=0, microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Gespräch {self.gespraechs_id} für {self.firmen_id.firma}"

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_count = models.IntegerField(default=0)  # Anzahl der fehlgeschlagenen Versuche
    last_attempt_time = models.DateTimeField(null=True, blank=True)  # Zeit des letzten Versuchs
    is_locked = models.BooleanField(default=False)  # Ist der Zugang gesperrt?
    lock_time = models.DateTimeField(null=True, blank=True)  # Bis wann gesperrt?

    def __str__(self):
        return f"{self.user.username} - Versuche: {self.attempt_count}"

# Create your models here.
