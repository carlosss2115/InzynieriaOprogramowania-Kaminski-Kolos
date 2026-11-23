# Dobór technologii – System Zarządzania Salonem Optycznym (SZSO) Opto-med

## Zestaw technologii i role w projekcie

| Obszar | Wybrana technologia i wersja | Rola w projekcie |
| :--- | :--- | :--- |
| **Widoki (Frontend)** | HTML5, CSS3, JavaScript (ES6) | Budowa responsywnych formularzy (logowanie, rezerwacja wizyty, koszyk zamówienia), katalogu okularów oraz obsługa interakcji UI (np. przełącznik podglądu hasła „POKAŻ”). |
| **Serwer (Backend)** | Python 3.12 + Flask 3.x | Obsługa routingu HTTP, sesji użytkowników (Pacjent, Optyk), walidacja formularzy po stronie serwera, weryfikacja kolizji terminów wizyt oraz aktualizacja stanów magazynowych. |
| **Baza danych** | SQLite 3 (moduł standardowy `sqlite3`) | Trwałe przechowywanie danych o użytkownikach, pacjentach, okularach, wizytach i zamówieniach w lokalnym pliku bazy z wymuszoną integralnością kluczy obcych (`PRAGMA foreign_keys = ON`). |
| **Praca zespołu** | Visual Studio Code, Git, GitHub | Edycja kodu źródłowego, kontrola wersji, podział zadań w zespole dwuosobowym oraz dokumentowanie postępów prac. |

## Uzasadnienie wyboru

Wybrany stos technologiczny oparty na języku Python, mikroframeworku Flask oraz bazie SQLite pozwala na szybkie uruchomienie aplikacji webowej lokalnie bez konieczności instalowania zewnętrznych serwerów bazodanowych ani korzystania z płatnych usług chmurowych. 
Moduł `sqlite3` jest wbudowany w standardową bibliotekę Pythona, co eliminuje problemy z konfiguracją środowiska na komputerach obu członków zespołu i gwarantuje pełną trwałość danych w jednym pliku. 
Flask zapewnia przejrzystą separację warstwy prezentacji (szablony Jinja2 w HTML/CSS) od logiki kontrolerów i encji bazodanowych, co bezpośrednio odwzorowuje wzorzec Boundary–Control–Entity zaprojektowany w dokumentacji UML systemu Opto-med. 
Zastosowanie czystego HTML5, CSS3 i podstawowego JavaScriptu umożliwia wierne odwzorowanie przygotowanych makiet GUI (formularza logowania, katalogu oraz koszyka) bez narzutu złożonych frameworków frontendowych. 
Dodatkowym atutem tego rozwiązania jest prosta składnia oraz łatwe debugowanie błędów po stronie serwera. Całość wspierana przez system kontroli wersji Git i repozytorium GitHub umożliwia równoległą, bezpieczną pracę dwuosobowego zespołu nad kolejnymi funkcjami MVP.
