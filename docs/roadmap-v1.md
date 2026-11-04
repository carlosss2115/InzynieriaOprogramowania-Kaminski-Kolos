# Mapa Projektu (Roadmap) – Iteracja v1: OptoMed

## 1. Cel i zakres wersji v1
* **Tytuł projektu:** OptoMed – Zintegrowany system rezerwacji badań wzroku i e-commerce optyczny salonu „Opto-med”.
* **Główny odbiorca:** Pacjent poszukujący zakupu okularów i badania wzroku oraz personel salonu (Optyk, Specjalista, Administrator).
* **Cel v1 (w 4 zdaniach):** 
  W wersji v1 skupiamy się na uruchomieniu podstawowej ścieżki klienta oraz personelu salonu optycznego. Użytkownik ma możliwość zarejestrowania się i zalogowania do systemu oraz przeglądania katalogu oprawek okularowych i produktów w sklepie internetowym. Ponadto pacjent może sprawdzić wolne terminy i zarezerwować lub odwołać wizytę na badanie wzroku u optometrysty. Oczekiwanym efektem jest pełna cyfryzacja rezerwacji wizyt, usprawnienie obsługi klientów oraz ułatwienie pracownikom zarządzania magazynem i kartotekami.

* **Wybrane funkcje MVP:**
  * **F01:** Użytkownik może zalogować się do systemu z uwzględnieniem ról (Pacjent, Optyk, Specjalista, Administrator).
  * **F02:** Użytkownik może przeglądać katalog oprawek okularowych i produktów w sklepie internetowym.
  * **F03:** Pacjent może sprawdzić dostępne terminy i zarezerwować/odwołać wizytę u optometrysty.
  * **F04:** Optyk może zarządzać bazą produktową i stanami magazynowymi (oprawy, soczewki).
  * **F05:** Specjalista (optometrysta) może prowadzić kartotekę pacjentów, historię badań oraz wystawiać recepty.

* **Odkładamy do v2:** Płatności elektroniczne online, koszyk zakupowy i finalizacja zamówień e-commerce oraz automatyczne powiadomienia SMS.

---

## 2. Widoki (Jak to ma wyglądać?)
W v1 projektujemy główne widoki interfejsu (GUI):

* **W01: Strona Główna i Katalog Produktów (Dla Gościa / Pacjenta)**
  * **Cel:** Prezentacja oferty salonu oraz przeglądanie dostępnych oprawek okularowych.
  * **Elementy:** Menu nawigacyjne (kategorie produktów), wyszukiwarka, siatka produktów (zdjęcie, nazwa, cena), odnośnik do logowania i rezerwacji wizyt.
  * **Dane wyświetlane:** Tabela `Okulary` (marka, model, typ_szkieł, cena).

* **W02: Formularz Logowania i Rejestracji (Dla Użytkowników)**
  * **Cel:** Uwierzytelnianie użytkownika w systemie i nadanie odpowiednich uprawnień.
  * **Elementy:** Pola E-mail (login) i Hasło, przycisk „Zaloguj się”, opcja „Pokaż” hasło oraz odnośniki do rejestracji i odzyskiwania dostępu.
  * **Dane wejściowe:** Login, hasło.

* **W03: Kalendarz i Rezerwacja Wizyty (Dla Pacjenta)**
  * **Cel:** Wybór dogodnego terminu badania wzroku u optometrysty.
  * **Elementy:** Widok kalendarza, lista dostępnych godzin u specjalisty, formularz potwierdzenia rezerwacji.
  * **Dane wprowadzane/wyświetlane:** Data, godzina, przypisany pacjent i specjalista.
  * **Komunikaty:**
    * *Poprawne działanie:* „Wizyta została pomyślnie zarezerwowana.”
    * *Błąd:* „Wybrany termin jest zajęty. Wybierz inną godzinę.”

---

## 3. Struktura bazy danych (Jakie dane zapisujemy?)
Baza danych opiera się na relacjach zaprojektowanych w poprzednim semestrze:

* **Tabela `Użytkownik`**
  * `id_użytkownika` (INT, PK)
  * `login` / `email` (VARCHAR)
  * `haslo` (VARCHAR)
  * `rola` (VARCHAR) – np. Pacjent, Optyk, Specjalista, Administrator
* **Tabela `Pacjent`**
  * `id_pacjenta` (INT, PK)
  * `id_użytkownika` (INT, FK)
  * `imie`, `nazwisko`, `telefon`, `adres`
* **Tabela `Okulary`**
  * `id_okularow` (INT, PK)
  * `marka`, `model`, `typ_szkiel`, `cena` (DECIMAL)
* **Tabela `Wizyty` / `Zamowienie`**
  * Powiązania dla rezerwacji terminów i ewidencji zleceń okularowych.

---

## 4. Opis funkcjonalności (Co i jak ma działać?)

* **F01 - Logowanie do systemu**
  * *Użytkownik:* Dowolna rola (Pacjent, Optyk, Specjalista, Administrator).
  * *Działanie:* Wprowadza e-mail i hasło; system weryfikuje dane i przekierowuje do właściwego panelu.
  * *Warunek poprawności:* Zgodność hasła (hash) w bazie; przy błędzie komunikat o nieprawidłowych danych.

* **F02 - Przeglądanie katalogu oprawek**
  * *Użytkownik:* Klient / Pacjent.
  * *Działanie:* Wyświetlanie listy dostępnych oprawek z bazy danych w widoku sklepu.
  * *Warunek poprawności:* Poprawne pobranie rekordów z tabeli `Okulary`.

* **F03 - Rezerwacja wizyty u optometrysty**
  * *Użytkownik:* Pacjent.
  * *Działanie:* Wybór wolnego terminu w kalendarzu i zapisanie rezerwacji w systemie.
  * *Warunek poprawności:* Wybrany termin nie koliduje z inną wizytą w bazie danych.

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
W wersji v2 planujemy rozwinięcie systemu o procesy e-commerce oraz automatyzację:
1. **Koszyk zakupowy i zamówienia:** Umożliwienie dodawania okularów do koszyka i składania zamówień online.
   * *Zmiana w widokach:* Dodanie widoku koszyka i formularza danych dostawy.
   * *Zmiana w danych:* Wykorzystanie tabel `Zamowienie`, `Faktura` i `Dostawa`.
2. **Powiadomienia SMS dla pacjentów:** Automatyczne wysyłanie wiadomości z przypomnieniem o zarezerwowanej wizycie.
