# OptoMed – System Zarządzania Salonem Optycznym

## Tytuł projektu
OptoMed – Zintegrowany system rezerwacji badań wzroku i e-commerce optyczny salonu „Opto-med”.

## Zespół
- **Nazwa zespołu:** Grupa 1 (Informatyka Ogólna)
- **Członkowie zespołu:**
  1. Jakub Kolos, nr indeksu: 180595, grupa: Laboratoryjna 1, GitHub: kolos21
  2. Marek Kamiński, nr indeksu: 182738, grupa: Laboratoryjna 1, GitHub: carlosss2115

## Idea i problem
Tradycyjne salony optyczne borykają się z problemem nieefektywnej obsługi klientów, którzy tracą czas na długie oczekiwanie w kolejkach oraz skomplikowany, telefoniczny proces umawiania badań wzroku. Ponadto proces zakupu oprawek i zarządzania kartotekami pacjentów w wielu miejscach wciąż opiera się na tradycyjnych, papierowych lub niepołączonych metodach, co generuje pomyłki i wydłuża czas obsługi. Naszym rozwiązaniem jest system **OptoMed**, który integruje platformę e-commerce z kalendarzem rezerwacji wizyt u optometrystów oraz pełną obsługą magazynową. Aplikacja umożliwia klientom wygodny przegląd katalogu okularów, zakup produktów online oraz rezerwację terminów badań wzroku, a personelowi salonu zapewnia narzędzia do zarządzania zleceniami i kartotekami. Oczekiwaną korzyścią jest pełna cyfryzacja salonu optycznego, oszczędność czasu pacjentów oraz usprawnienie pracy personelu.

## Użytkownicy i scenariusz
- **Główna grupa odbiorców:** Pacjenci/Klienci poszukujący zakupu okularów i badań wzroku oraz personel salonu (Administrator, Optyk, Specjalista/Optometrysta).
- **Przykładowy scenariusz użycia:** 
  1. Pacjent wchodzi na portal OptoMed i loguje się na swoje konto.
  2. Przegląda katalog oprawek okularowych i wybiera interesujący go model z bazy produktów.
  3. Następnie za pomocą zintegrowanego kalendarza rezerwuje termin badania wzroku u optometrysty.
  4. Efekt: Pacjent pojawia się na wizycie o wybranej godzinie, specjalista ma gotowy wgląd w jego profil, a proces zakupu okularów przebiega sprawnie i bezbłędnie.

## Zakres funkcjonalny
| ID | Funkcjonalność | Zakres |
| :--- | :--- | :--- |
| **F01** | Użytkownik może zalogować się do systemu z uwzględnieniem ról (Pacjent, Optyk, Specjalista, Administrator). | MVP |
| **F02** | Użytkownik może przeglądać katalog oprawek okularowych i produktów w sklepie internetowym. | MVP |
| **F03** | Pacjent może sprawdzić dostępne terminy i zarezerwować/odwołać wizytę u optometrysty. | MVP |
| **F04** | Optyk może zarządzać bazą produktową i stanami magazynowymi (oprawy, soczewki). | MVP |
| **F05** | Specjalista (optometrysta) może prowadzić kartotekę pacjentów, historię badań oraz wystawiać recepty. | MVP |
| **F06** | Użytkownik może sprawdzić aktualny status swojego zlecenia/zamówienia online. | Rozszerzenie |
| **F07** | System obsługuje płatności elektroniczne oraz automatyczne powiadomienia SMS. | Rozszerzenie |

## Poza zakresem
1. Integracja z systemami Narodowego Funduszu Zdrowia (NFZ) w celu automatycznego rozliczania refundacji na szkła korekcyjne w pierwszej wersji aplikacji.
2. Zaawansowany, dedykowany moduł księgowy dla wielu oddziałów firmy (wersja opiera się na uproszczonym fakturowaniu i ewidencji zamówień).

## Organizacja współpracy
- **Wstępny podział zadań:** 
  * *Jakub Kolos:* Architektura techniczna, modelowanie danych (ERD, diagramy klas), implementacja logiki backendowej i bazy danych.
  * *Marek Kamiński:* Analiza biznesowa, specyfikacja wymagań, makiety interfejsów (GUI) oraz implementacja warstwy widoku.
- **Sposób kontaktu:** Bieżąca komunikacja zespołu realizowana jest przez platformę LaboChat.com oraz dedykowany kanał roboczy.
- **Zasada aktualizacji:** Wszelkie zmiany w kodzie i dokumentacji są zatwierdzane poprzez commity w repozytorium GitHub, a kluczowe decyzje projektowe odnotowywane w zadaniach na LaboChat.com.

## Odnośniki
- **Repozytorium GitHub:** https://github.com/carlosss2115/InzynieriaOprogramowania-Kaminski-Kolos
- **Przestrzeń projektu (LaboChat.com):** make.labochat.com
