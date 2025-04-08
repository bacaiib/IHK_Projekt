from django import forms
from .models import Kunde, Vermerk

class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = ['firma', 'email', 'telefon_nr', 'fax_nr', 'anschrift', 'stadt', 'plz',  ]
        labels = {
            'firma': 'Firma',
            'email': 'E-Mail',
            'anschrift': 'Anschrift',
            'stadt': 'Ort',
            'plz': 'PLZ',
            'telefon_nr': 'Telefon-nr.:',
            'fax_nr': 'Fax-nr.:',

        }

class VermerkForm(forms.ModelForm):
    class Meta:
        model = Vermerk
        fields = ['firmen_id', 'kontaktart', 'anrede', 'name',
                  'betreff', 'gespraechsinhalt', 'wunsch', 'verfuegung']
        labels = {
            'firmen_id': 'Firma',
            'kontaktart': 'Kontaktart',
            'anrede': 'Anrede',
            'name': 'Name',
            'betreff': 'Betreff',
            'gespraechsinhalt': 'Gesprächsinhalt',  # Benutzerdefiniertes Label
            'wunsch': 'Wunsch',
            'verfuegung': 'Verfügung',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        self.fields['firmen_id'].choices = [('', 'Bitte wählen')] + \
            [("new", "Neuen Kunden anlegen")] + \
            list(Kunde.objects.values_list('kunden_nr', 'firma'))
        self.fields['firmen_id'].label = "Firma"