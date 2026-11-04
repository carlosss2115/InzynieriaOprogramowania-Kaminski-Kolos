# Mapa Projektu (Roadmap) – Iteracja v1: OptoMed

## 1. Cel i zakres wersji v1
* **Tytuł projektu:** OptoMed – System Zarządzania Salonem Optycznym z modułem AI.
* **Główny odbiorca:** Pacjent poszukujący badania wzroku i doboru okularów oraz personel salonu (Optyk, Specjalista)[cite: 5].
* **Cel v1:** 
  W wersji v1 skupiamy się na uruchomieniu podstawowej ścieżki klienta, która łączy nowoczesną technologię z tradycyjną obsługą salonu optycznego. Użytkownik ma możliwość zarejestrowania się i zalogowania do systemu oraz skorzystania z modułu AI do analizy kształtu twarzy ze zdjęcia, co pozwala na automatyczne dopasowanie i wyświetlenie rekomendowanych oprawek. Ponadto pacjent może samodzielnie sprawdzić wolne terminy i zarezerwować wizytę na badanie wzroku u optometrysty[cite: 9]. Oczekiwanym efektem jest skrócenie czasu wyboru okularów oraz sprawna rezerwacja wizyty bez konieczności kontaktu telefonicznego.

* **Wybrane funkcje MVP (zgodne z Lab 01):**
  * **F01:** Użytkownik może zalogować się do systemu z uwzględnieniem ról (Pacjent, Optyk, Specjalista)[cite: 5, 8].
  * **F02:** Użytkownik może wgrać zdjęcie w celu automatycznej analizy rysów twarzy i uzyskania rekomendacji oprawek przez AI.
  * **F03:** Pacjent może sprawdzić dostępne terminy i zarezerwować wizytę u optometrysty[cite: 9].
  * **F04:** Optyk może przeglądać i zarządzać bazą oprawek okularowych w magazynie[cite: 4, 7].
  * **F05:** Specjalista (optometrysta) może prowadzić kartotekę pacjentów i historię badań[cite: 8, 9].

* **Odkładamy do v2:** Płatności elektroniczne online, zaawansowany e-commerce (koszyk zakupowy, dostawy kurierskie) oraz powiadomienia SMS[cite: 5, 8].

---

## 2. Widoki (Jak to ma wyglądać?)
W v1 projektujemy 3 główne widoki interfejsu (GUI):

* **W01: Strona Główna / Panel Startowy (Dla Gościa / Pacjenta)**
  * **Cel:** Szybkie wprowadzenie do aplikacji oraz zachęcenie do skorzystania z AI lub rezerwacji wizyty.
  * **Elementy:** Nagłówek, menu nawigacyjne, baner zachęcający do testu AI („Dobierz oprawki ze zdjęciem”), przycisk rezerwacji wizyty, stopka.
  * **Dane:** Brak danych dynamicznych (widok statyczny/wizerunkowy).
  * **Przejścia:** Kliknięcie w test AI przenosi do W02; kliknięcie w rezerwację do W03.

* **W02: Moduł Analizy AI i Dopasowania Opraw (Dla Pacjenta)**
  * **Cel:** Wgranie zdjęcia twarzy i prezentacja dopasowanych przez algorytm oprawek.
  * **Elementy:** Formularz przesyłania pliku (zdjęcie), przycisk „Analizuj”, sekcja wyników z listą pasujących modeli okularów (zdjęcie, marka, model, cena)[cite: 16].
  * **Dane wejściowe:** Plik graficzny (zdjęcie użytkownika).
  * **Dane wyświetlane:** Tabela/lista `Okulary` (marka, model, typ_twarzy, cena)[cite: 16].
  * **Komunikaty:** 
    * *Poprawne działanie:* Wyświetlenie komunikatów o dopasowaniu i listy 3-5 oprawek.
    * *Błąd:* „Nieprawidłowy format pliku. Wgraj zdjęcie w formacie JPG lub PNG.”

* **W03: Kalendarz i Rezerwacja Wizyty (Dla Pacjenta)**
  * **Cel:** Wybór dogodnego terminu badania wzroku u optometrysty[cite: 9].
  * **Elementy:** Widok kalendarza miesięcznego/tygodniowego, lista dostępnych godzin, formularz potwierdzenia rezerwacji, przycisk „Potwierdź rezerwację”.
  * **Dane wprowadzane:** Data, godzina, ID pacjenta, ID specjalisty.
  * **Dane wyświetlane:** Dostępne sloty czasowe z tabeli `Grafik`/`Wizyty`[cite: 12].
  * **Komunikaty:**
    * *Poprawne działanie:* „Wizyta została pomyślnie zarezerwowana na dzień [Data] o godzinie [Godzina].”
    * *Błąd (zajęty termin):* „Wybrany termin jest już niedostępny. Wybierz inną godzinę.”

---

## 3. Struktura bazy danych (Jakie dane zapisujemy?)
Baza danych opiera się na kluczowych encjach wypracowanych w poprzednim semestrze[cite: 16]:

* **Tabela `Użytkownik`**
  * `id_użytkownika` (INT, PK)
  * `login` (VARCHAR(50))[cite: 16]
  * `haslo` (VARCHAR(255))[cite: 16]
  * `rola` (VARCHAR(20)) – np. Pacjent, Optyk, Specjalista[cite: 5, 8]
* **Tabela `Pacjent`**
  * `id_pacjenta` (INT, PK)
  * `id_użytkownika` (INT, FK)
  * `imie`, `nazwisko`, `telefon`, `email`[cite: 16]
* **Tabela `Okulary`**
  * `id_okularow` (INT, PK)
  * `marka`, `model`, `typ_twarzy` (VARCHAR)[cite: 16]
  * `cena` (DECIMAL)[cite: 16]
* **Tabela `Wizyty`**
  * `id_wizyty` (INT, PK)
  * `id_pacjenta` (INT, FK)
  * `data_czas` (DATETIME)
  * `status` (VARCHAR(50)) – np. Zaplanowana, Odwołana, Zakończona

*(Relacje: Jeden użytkownik/pacjent może mieć wiele wizyt[cite: 12]; oprawki są niezależnym katalogiem przeglądanym podczas analizy AI).*

---

## 4. Opis funkcjonalności (Co i jak ma działać?)

* **F01 - Logowanie do systemu**[cite: 5, 8]
  * *Użytkownik:* Gość / Pracownik / Pacjent.
  * *Działanie:* Wprowadza login i hasło w formularzu, system weryfikuje dane w tabeli `Użytkownik` i przekierowuje do odpowiedniego pulpitu[cite: 21].
  * *Widok:* Formularz logowania.
  * *Warunek poprawności:* Hash hasła w bazie zgadza się z podanym; w przypadku błędu system wyświetla komunikat „Nieprawidłowy login lub hasło”[cite: 8].

* **F02 - Dobór oprawek przez AI**
  * *Użytkownik:* Pacjent.
  * *Działanie:* Wgrywa zdjęcie w widoku W02, algorytm analizuje cechy twarzy i filtruje tabele `Okulary` na podstawie pola `typ_twarzy`[cite: 16].
  * *Widok:* W02 (Moduł AI).
  * *Warunek poprawności:* Zdjęcie zawiera wykrytą twarz, a zapytanie SQL zwraca minimum 1 pasujący model oprawek z bazy.

* **F03 - Rezerwacja wizyty**[cite: 9]
  * *Użytkownik:* Pacjent.
  * *Działanie:* Wybiera wolny termin w kalendarzu (W03), system zapisuje rekord w tabeli `Wizyty`.
  * *Widok:* W03 (Kalendarz wizyt)[cite: 12].
  * *Warunek poprawności:* Wybrana data i godzina nie są zajęte przez innego pacjenta (brak konfliktu w bazie danych).

---

## 5. Mapa zadań (Podział w zespole v1)

| Etap v1 | Od czego zależy? | Osoba odpowiedzialna | Termin | Oczekiwany rezultat |
| :--- | :--- | :--- | :--- | :--- |
| **Cel i zakres** | Pomysł z Lab 01 | Zespół (Jakub / Marek) | Tydzień 1 | Zatwierdzony cel v1 i lista funkcji MVP |
| **1. Widoki (GUI)** | Cel i zakres v1 | Marek Kamiński | Tydzień 1/2 | Szkice widoków W01, W02, W03 |
| **2. Struktura bazy** | Wymagania widoków | Jakub Kolos | Tydzień 2 | Schemat tabel i relacji SQL dla v1 |
| **3. Funkcjonalności** | Widok i baza | Zespół | Tydzień 2/3 | Opis logiki F01, F02, F03 |
| **Sprawdzenie spójności**| Wszystkie etupy | Zespół | Tydzień 3 | Pełna dokumentacja v1 w `docs/roadmap-v1.md` |

---

## 6. Kierunek kolejnej iteracji (v2)
W wersji v2 planujemy rozwinięcie systemu o dwa kluczowe elementy e-commerce:
1. **Koszyk i moduł zamówień internetowych:** Umożliwienie bezpośredniego zakupu dobranych przez AI okularów online.
   * *Zmiana w widokach:* Dodanie widoku koszyka i formularza płatności (wzorowanego na makietach z poprzedniego semestru)[cite: 18].
   * *Zmiana w danych:* Wykorzystanie tabel `Zamowienie`, `Faktura` i `Dostawa` z poprzedniej dokumentacji[cite: 16].
   * *Zmiana w funkcjach:* Obsługa płatności elektronicznych i generowanie zlecenia warsztatowego dla optyka[cite: 4, 8].
2. **Automatyczne powiadomienia SMS:** Wysyłanie przypomnień o zbliżającej się wizycie do pacjenta.
   * *Zmiana w widokach:* Brak zmian w GUI (funkcja w tle).
   * *Zmiana w danych:* Dodanie pola statusu powiadomienia w tabeli `Wizyty`.
   * *Zmiana w funkcjach:* Integracja z zewnętrzną bramką SMS po pomyślnym zarezerwowaniu terminu (F03).
