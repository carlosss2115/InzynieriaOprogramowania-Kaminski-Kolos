# OptoMed – System Zarządzania Salonem Optycznym z AI

## Tytuł projektu
OptoMed – System Zarządzania Salonem Optycznym z modułem AI do doboru oprawek i rezerwacji badań wzroku.

## Zespół
* **Nazwa zespołu:** Grupa 1 (Informatyka Ogólna)[cite: 4]
* **Członkowie zespołu:**
  1. Jakub Kolos, nr indeksu: [Wpisz numer], grupa: Laboratoryjna 1, GitHub: [@JakubKolos]
  2. Marek Kamiński, nr indeksu: [Wpisz numer], grupa: Laboratoryjna 1, GitHub: [@MarekKaminski]

## Idea i problem
Tradycyjne salony optyczne borykają się z problemem nieefektywnej obsługi klientów, którzy tracą czas na długie oczekiwanie w kolejkach oraz skomplikowany, telefoniczny proces umawiania badań wzroku. Ponadto dobór odpowiednich oprawek bywa dla pacjentów przytłaczający ze względu na brak spersonalizowanego doradztwa i trudność w ocenie, jak dany model pasuje do rysów twarzy. Obecnie większość tych procesów opiera się na tradycyjnych metodach, takich jak wizyty stacjonarne, ręczne przeglądanie katalogów czy papierowe kartoteki, co generuje błędy i wydłuża czas obsługi. Naszym rozwiązaniem jest rozbudowa systemu **OptoMed** o zaawansowane moduły sztucznej inteligencji, które automatyzują proces wstępnego doboru oprawek na podstawie analizy kształtu twarzy ze zdjęcia użytkownika. Zintegrowany kalendarz online umożliwia błyskawiczne umawianie wizyt u optometrystów[cite: 5, 9], a cyfrowy magazyn i e-commerce spinają całą ścieżkę klienta w jeden spójny ekosystem[cite: 4, 16]. Oczekiwaną korzyścią jest pełna cyfryzacja salonu, oszczędność czasu personelu i pacjentów oraz unikalne, spersonalizowane doświadczenie zakupowe wspierane przez AI.

## Użytkownicy i scenariusz
* **Główna grupa odbiorców:** Pacjenci/Klienci poszukujący zakupu okularów i badań wzroku oraz personel salonu (Administrator, Optyk, Specjalista/Optometrysta)[cite: 5].
* **Przykładowy scenariusz użycia:** 
  1. Pacjent wchodzi na portal OptoMed i wgrywa swoje zdjęcie do modułu AI, który analizuje proporcje i kształt twarzy.
  2. System automatycznie dopasowuje i proponuje najlepiej pasujące oprawki z bazy produktów[cite: 16].
  3. Użytkownik wybiera model, a następnie za pomocą zintegrowanego kalendarza rezerwuje termin badania wzroku u optometrysty[cite: 9].
  4. Efekt: Pacjent pojawia się na wizycie o wybranej godzinie, specjalista ma gotowy wgląd w jego profil, a proces zakupu okularów przebiega szybko i bezbłędnie[cite: 8, 9].

## Zakres funkcjonalny
| ID | Funkcjonalność | Zakres |
| :--- | :--- | :--- |
| **F01** | Użytkownik może zalogować się do systemu z uwzględnieniem ról (Pacjent, Optyk, Specjalista, Administrator)[cite: 5, 8]. | MVP |
| **F02** | Użytkownik może wgrać zdjęcie w celu automatycznej analizy kształtu twarzy i uzyskania rekomendacji oprawek przez AI. | MVP |
| **F03** | Pacjent może sprawdzić dostępne terminy i zarezerwować/odwołać wizytę u optometrysty[cite: 9]. | MVP |
| **F04** | Optyk może zarządzać bazą produktową i stanami magazynowymi (oprawy, soczewki)[cite: 4, 7]. | MVP |
| **F05** | Specjalista (optometrysta) może prowadzić kartotekę pacjentów, historię badań oraz wystawiać recepty[cite: 8, 9]. | MVP |
| **F06** | Użytkownik może sprawdzić aktualny status swojego zlecenia/zamówienia online[cite: 9]. | Rozszerzenie |
| **F07** | System obsługuje płatności elektroniczne oraz automatyczne powiadomienia SMS[cite: 5, 8]. | Rozszerzenie |

## Poza zakresem
1. Integracja z systemami Narodowego Funduszu Zdrowia (NFZ) w celu automatycznego rozliczania refundacji na szkła korekcyjne w pierwszej wersji aplikacji.
2. Zaawansowany, dedykowany moduł księgowy dla wielu oddziałów firmy (wersja opiera się na uproszczonym fakturowaniu i ewidencji zamówień)[cite: 15].

## Organizacja współpracy
* **Wstępny podział zadań:** 
  * *Jakub Kolos:* Architektura techniczna, modelowanie danych (ERD, diagramy klas)[cite: 21], implementacja logiki backendowej i bazy danych.
  * *Marek Kamiński:* Analiza biznesowa, specyfikacja wymagań, makiety interfejsów (GUI) oraz implementacja warstwy widoku i modułu AI[cite: 21].
* **Sposób kontaktu:** Bieżąca komunikacja zespołu realizowana jest przez platformę LaboChat.com[cite: 2] oraz dedykowany kanał roboczy.
* **Zasada aktualizacji:** Wszelkie zmiany w kodzie i dokumentacji są zatwierdzane poprzez commity w repozytorium GitHub, a kluczowe decyzje projektowe odnotowywane w zadaniach na LaboChat.com[cite: 2].

## Odnośniki
* **Repozytorium GitHub:** [Wpisz link do swojego repozytorium][cite: 2]
* **Przestrzeń projektu (LaboChat.com):** [Wpisz link do LaboChat.com][cite: 2]
