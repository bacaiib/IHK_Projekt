from django import forms
from .models import Kunde, Vermerk

class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = ['firma', 'anschrift', 'telefon_nr', 'fax_nr', 'email', 'stadt']

class VermerkForm(forms.ModelForm):
    class Meta:
        model = Vermerk
        fields = ['firmen_id', 'kontaktart', 'anrede', 'name',
                  'betreff', 'gespraechsinhalt', 'wunsch', 'aufgenommen', 'verfuegung']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        self.fields['firmen_id'].choices = [('', 'Bitte wählen')] + \
            [("new", "Neuen Kunden anlegen")] + \
            list(Kunde.objects.values_list('kunden_nr', 'firma'))
        self.fields['firmen_id'].label = "Firma"