function toggleSearchField() {
  var filterType = document.getElementById('filter_type').value;
  var searchTermContainer = document.getElementById('search_term_container');
  var wunschContainer = document.getElementById('wunsch_container');
  var kontaktartContainer = document.getElementById('kontaktart_container');
  var anredeContainer = document.getElementById('anrede_container');
  var firmaContainer = document.getElementById('firma_container');

  // Alle Eingabefelder holen
  var searchTermInput = document.getElementById('search_term');
  var wunschSelect = document.getElementById('wunsch_select');
  var kontaktartSelect = document.getElementById('kontaktart_select');
  var anredeSelect = document.getElementById('anrede_select');
  var firmaSelect = document.getElementById('firma_select');

  // Alle Container ausblenden und Eingabefelder deaktivieren
  searchTermContainer.style.display = 'none';
  wunschContainer.style.display = 'none';
  kontaktartContainer.style.display = 'none';
  anredeContainer.style.display = 'none';
  firmaContainer.style.display = 'none';

  searchTermInput.disabled = true;
  wunschSelect.disabled = true;
  kontaktartSelect.disabled = true;
  anredeSelect.disabled = true;
  firmaSelect.disabled = true;

  // Den passenden Container anzeigen und Eingabefeld aktivieren
  if (filterType === 'wunsch') {
    wunschContainer.style.display = 'block';
    wunschSelect.disabled = false;
  } else if (filterType === 'kontaktart') {
    kontaktartContainer.style.display = 'block';
    kontaktartSelect.disabled = false;
  } else if (filterType === 'anrede') {
    anredeContainer.style.display = 'block';
    anredeSelect.disabled = false;
  } else if (filterType === 'firma') {
    firmaContainer.style.display = 'block';
    firmaSelect.disabled = false;
  } else {
    searchTermContainer.style.display = 'block';
    searchTermInput.disabled = false;
  }
}

// Beim Laden der Seite das richtige Feld anzeigen
window.onload = function() {
  toggleSearchField();
};