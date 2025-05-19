from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Kunde, Vermerk
from .forms import KundeForm, VermerkForm
from django.utils import timezone


def index(request):
    return render(request, 'index.html')

@login_required
@never_cache
def logout_view(request):
    logout(request)  # Benutzer ausloggen
    messages.success(request, "Sie haben sich erfolgreich ausgeloggt!")  # Erfolgsmeldung
    return redirect('logout_success')  # Weiterleitung zur Erfolgsseite

def logout_success(request):
    return render(request, 'logout_success.html')  # Rendert die Erfolgsseite

def kunde_edit(request, pk):
    kunde = get_object_or_404(Kunde, pk=pk)
    if request.method == 'POST':
        form = KundeForm(request.POST, instance=kunde)
        if form.is_valid():
            form.save()
            return redirect('kunden_detail', kunden_nr=kunde.pk)
    else:
        form = KundeForm(instance=kunde)
    return render(request, 'kunde_bearbeiten.html', {'form': form, 'kunde': kunde})

def vermerk_edit(request, pk):
    vermerk = get_object_or_404(Vermerk, pk=pk)
    if request.method == 'POST':
        form = VermerkForm(request.POST, instance=vermerk)
        if form.is_valid():
            form.save()
            return redirect('vermerk_detail', gespraechs_id=vermerk.gespraechs_id)
    else:
        form = VermerkForm(instance=vermerk)
    return render(request, 'vermerk_bearbeiten.html', {'form': form, 'vermerk': vermerk})

@login_required
@never_cache
def kunden_uebersicht(request):
        # Standardmäßig nach Name filtern, falls nichts angegeben
        filter_type = request.GET.get('filter_type', '')
        search_term = request.GET.get('search_term', '')
        kunden = Kunde.objects.all()
        # Filterlogik basierend auf dem ausgewählten Filtertyp
        if search_term:
            if filter_type == 'firma':
                kunden = kunden.filter(firma__icontains=search_term)
            elif filter_type == 'email':
                kunden = kunden.filter(email__icontains=search_term)
            elif filter_type == 'anschrift':
                kunden = kunden.filter(anschrift__icontains=search_term)
            elif filter_type == 'stadt':
                kunden = kunden.filter(stadt__icontains=search_term)
            elif filter_type == 'telefon_nr':
                kunden = kunden.filter(telefon_nr__icontains=search_term)
            elif filter_type == 'fax_nr':
                kunden = kunden.filter(fax_nr__icontains=search_term)

        context = {
            'kunden': kunden,
            'filter_type': filter_type,
            'search_term': search_term,
        }
        return render(request, 'kunden_uebersicht.html',context)



@login_required
@never_cache
def vermerk_uebersicht(request):
    # Filtertyp und Suchbegriff aus GET-Parametern holen
    filter_type = request.GET.get('filter_type', 'name')
    search_term = request.GET.get('search_term', '')

    print(f"Filter Type: {filter_type}")
    print(f"Search Term: {search_term}")

    vermerke = Vermerk.objects.all()
    print(f"Anzahl Vermerke vor Filter: {vermerke.count()}")

    if search_term:  # Nur filtern, wenn search_term nicht leer ist
        if filter_type == 'wunsch':
            vermerke = vermerke.filter(wunsch__iexact=search_term)
            print(f"Filter wunsch__iexact={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'kontaktart':
            vermerke = vermerke.filter(kontaktart__iexact=search_term)
            print(f"Filter kontaktart__iexact={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'anrede':
            vermerke = vermerke.filter(anrede__iexact=search_term)
            print(f"Filter anrede__iexact={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'name':
            vermerke = vermerke.filter(name__icontains=search_term)
            print(f"Filter name__icontains={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'betreff':
            vermerke = vermerke.filter(betreff__icontains=search_term)
            print(f"Filter betreff__icontains={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'gespraechsinhalt':
            vermerke = vermerke.filter(gespraechsinhalt__icontains=search_term)
            print(f"Filter gespraechsinhalt__icontains={search_term}, Ergebnisse: {vermerke.count()}")
        elif filter_type == 'firma':
            try:
                firmen_id_int = int(search_term)
                vermerke = vermerke.filter(firmen_id=firmen_id_int)
                print(f"Filter firmen_id={firmen_id_int}, Ergebnisse: {vermerke.count()}")
            except ValueError:
                print(f"Ungültige firmen_id: {search_term}")

    print(f"Anzahl Vermerke nach Filter: {vermerke.count()}")

    wunsch_choices = Vermerk._meta.get_field('wunsch').choices
    kontaktart_choices = Vermerk._meta.get_field('kontaktart').choices
    anrede_choices = Vermerk._meta.get_field('anrede').choices
    kunden = Kunde.objects.all()

    return render(request, 'vermerk_uebersicht.html', {
        'vermerke': vermerke,
        'filter_type': filter_type,
        'search_term': search_term,
        'wunsch_choices': wunsch_choices,
        'kontaktart_choices': kontaktart_choices,
        'anrede_choices': anrede_choices,
        'kunden': kunden,
    })

@login_required
@never_cache
def kunden_detail(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    return render(request, 'kunden_detail.html', {'kunde': kunde})

@login_required
@never_cache
def vermerk_detail(request, gespraechs_id):
    vermerk = get_object_or_404(Vermerk, gespraechs_id=gespraechs_id)
    return render(request, 'vermerk_detail.html', {'vermerk': vermerk})

@login_required
@never_cache
def kunde_neu(request):
    if request.method == "POST":
        form = KundeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kunden-uebersicht')
    else:
        form = KundeForm()
    return render(request, 'kunde_neu.html', {'form': form})

@login_required
@never_cache
def kunde_loeschen(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    if request.method == 'POST':
        kunde.delete()
        return redirect('kunden-uebersicht')
    return redirect('kunden-uebersicht')

@login_required
@never_cache
def vermerk_loeschen(request, gespraechs_id):
    vermerk = get_object_or_404(Vermerk, gespraechs_id=gespraechs_id)
    if request.method == 'POST':
        vermerk.delete()
        return redirect('vermerk-uebersicht')
    return redirect('vermerk-uebersicht')

@login_required
@never_cache
def vermerk_erfassen(request):
    if request.method == "POST":
        form = VermerkForm(request.POST)
        if form.is_valid():
                vermerk = form.save(commit=False)  # Vermerk noch nicht speichern
                vermerk.aufgenommen = request.user.username  # Nutzername wird gespeichert
                form.save()  # Jetzt speichern
                return redirect('vermerk-uebersicht')  # Weiterleitung zur Übersicht
    else:
        initial_data = {}
        kunden_nr = request.GET.get('kunden_nr')
        if kunden_nr:
            kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr) # Kunden-Nr. aus URL holen
            initial_data = {
                'firmen_id': kunde.kunden_nr,  # Vorbelegung des Kundenfeldes
            }
        initial_data['datum'] = timezone.now()  # Aktuelles Datum vorbelegen
        form = VermerkForm(initial=initial_data)
    return render(request, 'vermerk_erfassen.html', {'form': form})

@login_required
@never_cache
def get_kunde_data(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    data = {
        'firma': kunde.firma,
        'anschrift': kunde.anschrift,
        'telefon_nr': kunde.telefon_nr,
        'fax_nr': kunde.fax_nr,
    }
    return JsonResponse(data)

# Create your views here.
