# Dobór technologii – OptoMed (SZSO Opto-med v1)

## Zestaw technologii i role w projekcie

| Obszar | Wybrana technologia i wersja | Rola w projekcie |
| :--- | :--- | :--- |
| **Widoki (Frontend)** | HTML5, CSS3, JavaScript (ES6) | Budowa widoków W01 (katalog oprawek z wyszukiwarką), W02 (logowanie z przyciskiem „Pokaż” i rejestracja), W03 (rezerwacja wizyt) oraz paneli Optyka i Specjalisty. |
| **Serwer (Backend)** | Python 3.12 + Flask 3.x | Obsługa sesji i ról (`Pacjent`, `Optyk`, `Specjalista`, `Administrator`), walidacja danych, sprawdzanie kolizji terminów wizyt oraz obsługa kartoteki badań i magazynu. |
| **Baza danych** | SQLite 3 (moduł `sqlite3`) | Trwałe przechowywanie danych w lokalnym pliku `optomed.db` z włączoną obsługą kluczy obcych (`PRAGMA foreign_keys = ON`). |
| **Praca zespołu** | Visual Studio Code, Git, GitHub | Edycja kodu źródłowego, historia zmian, podział pracy między członkami zespołu oraz utrzymanie dokumentacji w katalogu `docs/`. |

## Uzasadnienie wyboru

Zestaw oparty na języku Python, mikroframeworku Flask oraz bazie SQLite umożliwia natychmiastowe uruchomienie systemu OptoMed lokalnie na komputerach obu członków zespołu bez instalowania zewnętrznych serwerów bazodanowych i bez płatnych usług chmurowych. Moduł `sqlite3` jest wbudowany w standardową bibliotekę Pythona, co eliminuje problemy konfiguracyjne i gwarantuje trwały zapis rezerwacji wizyt, asortymentu oraz recept w jednym pliku bazy danych. Flask zapewnia przejrzyste oddzielenie warstwy prezentacji (szablony HTML w Jinja2) od logiki kontrolerów i zapytań SQL, co bezpośrednio odpowiada architekturze Boundary–Control–Entity z naszej dokumentacji UML. Wykorzystanie czystego HTML5, CSS3 oraz prostego JavaScriptu pozwala wiernie odwzorować makiety GUI (katalogu produktów, formularza logowania i kalendarza wizyt) bez narzutu złożonych bibliotek frontendowych. Prosta struktura projektu ułatwia testowanie reguł walidacji po stronie serwera, takich jak wykrywanie kolizji terminów u optometrysty. Całość wspierana przez system Git i platformę GitHub pozwala wygodnie dzielić zadania oraz śledzić postępy iteracji v1.
