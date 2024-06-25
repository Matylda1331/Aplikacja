import pygame
import sys
import random
import time
from typing import List, Optional, Tuple, Set, Union

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WYSOKOSC_OKNA: int = 650
SZEROKOSC_OKNA: int = 510
KOLUMNY: int = 5
RZEDY: int = 6
ROZMIAR_OKNA: int = 100
BRZEG: int = 5
TLO: Tuple[int, int, int] = (255, 255, 255)

# Kolory używane w grze
CZARNY: Tuple[int, int, int] = (0, 0, 0)
SZARY: Tuple[int, int, int] = (155, 155, 155)
ZOLTY: Tuple[int, int, int] = (255, 255, 153)
ZIELONY: Tuple[int, int, int] = (111, 169, 111)
BIALY: Tuple[int, int, int] = (255, 255, 255)
CZERWONY: Tuple[int, int, int] = (255, 50, 30)
ROZOWY: Tuple[int, int, int] = (255, 153, 204)

# Czcionki używane w grze
CZCIONKA_DUZA: pygame.font.Font = pygame.font.SysFont('times new roman', 68)
CZCIONKA_MALA: pygame.font.Font = pygame.font.SysFont('times new roman', 28)
CZCIONKA_CZAS: pygame.font.Font = pygame.font.SysFont('times new roman', 28)

class WordleGame:
    def __init__(self) -> None:
        # Inicjalizacja okna gry
        self.okno: pygame.Surface = pygame.display.set_mode((SZEROKOSC_OKNA, WYSOKOSC_OKNA), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")
        # Listy słów
        self.mozliwe_hasla = self.lista_hasel()
        self.haslo: str = random.choice(self.mozliwe_hasla) # Losowe hasło
        self.proby: List[List[str]] = [[''] * KOLUMNY for _ in range(RZEDY)]
        self.kolory: List[List[Tuple[int, int, int]]] = [[BIALY] * KOLUMNY for _ in range(RZEDY)]
        self.proba_teraz: str = ''
        self.rzad: int = 0
        self.start_czas: Optional[float] = None
        self.limit_czasu: Optional[float] = None
        self.komunikat: Optional[str] = None
        self.licznik_slow: int = 0

    from listy_slow import lista_hasel # Import listy haseł
    from listy_slow import lista_slow # Import listy słów

    def sprawdzanie(self, proba: str) -> Tuple[Set[Tuple[str, int]], Set[Tuple[str, int]], Set[Tuple[str, int]]]:
        """Porównuje aktualną próbę gracza z odgadywanym hasłem.
        
        Dla słowa wpisanego przez użytkownika, funkcja zwraca zbiory krotek '(litera, indeks)';
        zielone -- poprawne litery na poprawnych pozycjach,
        zolte -- poprawne litery na niepoprawnych pozycjach,
        szare -- niepoprawne litery.
        """
        zielone: Set[Tuple[str, int]] = set()
        zolte: Set[Tuple[str, int]] = set()
        szare: Set[Tuple[str, int]] = set()
        ile_w_hasle = {char: self.haslo.count(char) for char in self.haslo}  # Ile każdej litery w haśle
        zielone_indeksy: Set[int] = set()

        # Sprawdzenie, które litery są całkowicie poprawne(zielone)
        for i, char in enumerate(self.haslo):
            if char == proba[i]:
                zielone.add((proba[i], i))
                zielone_indeksy.add(i)
                ile_w_hasle[proba[i]] -= 1
        
        # Sprawdzenie, które litery są w haśle, ale nie są na poprawnym miejscu (żółtych) i jakich nie ma w haśle (szare)
        for i, char in enumerate(proba):
            if i not in zielone_indeksy:
                if char in self.haslo and ile_w_hasle.get(char, 0) > 0:
                    zolte.add((char, i))
                    ile_w_hasle[char] -= 1
                else:
                    szare.add((char, i))

        return zielone, zolte, szare
    
    def krata(self) -> None:
        """Rysuje kratę do gry."""
        self.okno.fill(TLO)
        for rzad in range(RZEDY):
            for kolumna in range(KOLUMNY):
                kwadraty = pygame.Rect(kolumna * ROZMIAR_OKNA + BRZEG, rzad * ROZMIAR_OKNA + BRZEG,
                    ROZMIAR_OKNA - BRZEG, ROZMIAR_OKNA - BRZEG)
                pygame.draw.rect(self.okno, CZARNY, kwadraty, 2)

    def tekst_w_kracie(self, tekst: str, czcionka: pygame.font.Font, kolor: Tuple[int, int, int], kwadrat: pygame.Rect) -> None:
        """Rysuje litery."""
        tekst_wierzch = czcionka.render(tekst, True, kolor)
        tekst_kwadrat = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def rysuj_tekst(self, pozostaly_czas: Optional[int] = None) -> None:
        """Rysuje elementy interfejsu na ekranie gry: kratę do gry, wprowadzone słowa, 
        litery wpisywane w bieżącej próbie, a w przypadku podania argumentu pozostaly_czas odliczanie czasu
        i liczbę odgadniętych słów.
        """
        # Rysowanie wprowadzonych słów
        for r, próba in enumerate(self.proby):
            for k, litera in enumerate(próba):
                kwadr = pygame.Rect(k * ROZMIAR_OKNA + BRZEG, r * ROZMIAR_OKNA + BRZEG, 
                    ROZMIAR_OKNA - BRZEG, ROZMIAR_OKNA - BRZEG)
                pygame.draw.rect(self.okno, self.kolory[r][k], kwadr)
                if litera:
                    self.tekst_w_kracie(litera, CZCIONKA_DUZA, CZARNY, kwadr)

        # Rysowanie bieżącej próby
        for i in range(KOLUMNY):
            kwadr = pygame.Rect(i * ROZMIAR_OKNA + BRZEG, self.rzad * ROZMIAR_OKNA + BRZEG,
                ROZMIAR_OKNA - BRZEG, ROZMIAR_OKNA - BRZEG)
            pygame.draw.rect(self.okno, BIALY, kwadr)
            if i < len(self.proba_teraz):
                self.tekst_w_kracie(self.proba_teraz[i], CZCIONKA_DUZA, CZARNY, kwadr)
            pygame.draw.rect(self.okno, CZARNY, kwadr, 2)

        # Rysowanie odliczania czasu i licznika słów
        if pozostaly_czas is not None:
            czas_minuty = pozostaly_czas // 60
            czas_sekundy = pozostaly_czas % 60
            czas_tekst = CZCIONKA_CZAS.render(f"{czas_minuty}:{czas_sekundy:02}", True, CZARNY)
            self.okno.blit(czas_tekst, (SZEROKOSC_OKNA - 100, WYSOKOSC_OKNA - 40))
            licznik_tekst = CZCIONKA_CZAS.render(f"Słowa: {self.licznik_slow}", True, CZARNY)
            self.okno.blit(licznik_tekst, (20, WYSOKOSC_OKNA - 40))

        # Aktualizacja czasu gry
        czas = self.aktualizuj_czas()
        if czas is not None:
            czas_tekst = CZCIONKA_CZAS.render(czas, True, CZARNY)
            self.okno.blit(czas_tekst, (20, WYSOKOSC_OKNA - 40))

        # Wyświetlanie błędu 
        if self.komunikat is not None and self.komunikat_czas is not None:
            if time.time() - self.komunikat_czas < 1.2:
                komunikat_prostokat = pygame.Rect(55, 220, 400, 50)
                pygame.draw.rect(self.okno, CZERWONY, komunikat_prostokat)
                komunikat_tekst = CZCIONKA_MALA.render(self.komunikat, True, CZARNY)
                komunikat_rect = komunikat_tekst.get_rect(center=komunikat_prostokat.center)
                self.okno.blit(komunikat_tekst, komunikat_rect)
            else:
                self.komunikat = None
                self.komunikat_czas = None

        # Dodanie przycisku MENU
        self.menu_button = pygame.Rect(SZEROKOSC_OKNA // 2 - 50, WYSOKOSC_OKNA - 37, 100, 30)
        pygame.draw.rect(self.okno, SZARY, self.menu_button)
        self.tekst_w_kracie("MENU", CZCIONKA_MALA, CZARNY, self.menu_button)

    def aktualizuj_czas(self) -> Optional[str]:
        """Aktualizuje czas gry i zwraca go w formacie MM:SS."""
        if self.start_czas is not None and self.tryb == "na_czas":
            ile_czasu = int(time.time() - self.start_czas)  # Oblicza upływający czas od startu gry
            czas_minuty = ile_czasu // 60
            czas_sekundy = ile_czasu % 60
            return f"{czas_minuty}:{czas_sekundy:02}"  # Formatuje czas jako "MM:SS".
        return None

    def pokaz_wiadomosc(self, wiadomosc: str) -> str:
        """Wyświetla wiadomość na ekranie wraz z dwoma przyciskami do wyboru akcji.
        Wyświetla podaną wiadomość na środku ekranu oraz dwa przyciski: "Wróć do menu" i "Zagraj ponownie". 
        Po wybraniu jednej z opcji przez użytkownika zwraca "menu" lub "ponownie".
        """
        while True:
            self.okno.fill(TLO)
            linie_wiadomosci = wiadomosc.split('\n')
            y = WYSOKOSC_OKNA // 2 - 50
            for linia in linie_wiadomosci:
                self.tekst_w_kracie(linia, CZCIONKA_MALA, CZARNY, pygame.Rect(0, y, SZEROKOSC_OKNA, 50))
                y += 50

            # Dodanie przycisków 
            przycisk_menu = pygame.Rect(SZEROKOSC_OKNA // 2 - 100, WYSOKOSC_OKNA // 2 + 100, 200, 50)
            przycisk_ponownie = pygame.Rect(SZEROKOSC_OKNA // 2 - 100, WYSOKOSC_OKNA // 2 + 170, 200, 50)
        
            pygame.draw.rect(self.okno, ROZOWY, przycisk_menu)
            pygame.draw.rect(self.okno, ROZOWY, przycisk_ponownie)

            self.tekst_w_kracie("Wróć do menu", CZCIONKA_MALA, CZARNY, przycisk_menu)
            self.tekst_w_kracie("Zagraj ponownie", CZCIONKA_MALA, CZARNY, przycisk_ponownie)

            pygame.display.flip()

            # Dodanie działania przycisków 
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    if przycisk_menu.collidepoint(zdarzenie.pos):
                        return "menu"
                    elif przycisk_ponownie.collidepoint(zdarzenie.pos):
                        return "ponownie"

    def main(self, tryb: str) -> None:
        """Główna funkcja gry. W zależności od trybu inicjalizuje ustawienia gry,
        rysuje interfejs, obsługuje zdarzenia PyGame.
        """
        self.tryb = tryb
        self.haslo = random.choice(self.mozliwe_hasla)
        self.proby: List[List[str]] = [[''] * KOLUMNY for _ in range(RZEDY)]
        self.kolory: List[List[str]] = [[BIALY] * KOLUMNY for _ in range(RZEDY)]
        self.proba_teraz: str = ''
        self.rzad: int = 0
        self.start_czas: Optional[float] = time.time() if tryb != "standard" else None
        self.limit_czasu: Optional[int] = 5 if tryb == "najwięcej_słów" else None  # Ustawienie czasu w trybie najwięcej słów
        self.komunikat: Optional[str] = None
        self.komunikat_czas: Optional[float] = None
        self.licznik_slow: int = 0

        while True:
            # Sprawdza pozostały czas
            if tryb != "standard" and tryb != "na_czas":
                pozostaly_czas: Optional[int] = max(0, self.limit_czasu - int(time.time() - self.start_czas)) if self.start_czas is not None else None
                if pozostaly_czas is not None and pozostaly_czas <= 0:
                    if tryb == "najwięcej_słów":
                        wynik = self.pokaz_wiadomosc(f"Koniec czasu. Słowa: {self.licznik_slow}")
                    if wynik == "ponownie":
                        self.main(tryb)
                    elif wynik == "menu":
                        return
                    return
            else:
                pozostaly_czas = None

            self.krata()  # Rysuje planszę gry.
            self.rysuj_tekst(pozostaly_czas)  # Rysuje pozostały czas.

            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:  # Sprawdza, czy użytkownik zamknął okno.
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.KEYDOWN:
                    if zdarzenie.key == pygame.K_BACKSPACE:
                        self.proba_teraz = self.proba_teraz[:-1]
                    elif zdarzenie.key == pygame.K_RETURN:
                        if len(self.proba_teraz) == KOLUMNY:  # Sprawdza, czy długość słowa jest zgodna.
                            if self.proba_teraz not in self.lista_slow():  # Sprawdza poprawność słowa.
                                self.komunikat = "Słowo niepoprawne"
                                self.komunikat_czas = time.time()
                            else:
                                self.komunikat = None
                                self.komunikat_czas = None
                                zielone, zolte, szare = self.sprawdzanie(self.proba_teraz)  # Sprawdza poprawność liter.
                                for i, litera in enumerate(self.proba_teraz):
                                    if (litera, i) in zielone:
                                        self.kolory[self.rzad][i] = ZIELONY
                                    elif (litera, i) in zolte:
                                        self.kolory[self.rzad][i] = ZOLTY
                                    elif (litera, i) in szare:
                                        self.kolory[self.rzad][i] = SZARY
                                self.proby[self.rzad] = list(self.proba_teraz)
                                self.rzad += 1
                                if self.proba_teraz == self.haslo:  # Sprawdza, czy słowo jest poprawne.
                                    if tryb == "najwięcej_słów":
                                        self.licznik_slow += 1
                                        self.rzad = 0
                                        self.proby = [[''] * KOLUMNY for _ in range(RZEDY)]
                                        self.kolory = [[BIALY] * KOLUMNY for _ in range(RZEDY)]
                                        self.proba_teraz = ''
                                        self.haslo = random.choice(self.mozliwe_hasla)
                                        continue
                                    elif tryb == "na_czas":
                                        ile_czasu = int(time.time() - self.start_czas)
                                        wynik = self.pokaz_wiadomosc(f"Gratulacje, hasło odgadnięte poprawnie. \n Czas: {ile_czasu // 60}:{ile_czasu % 60:02} \n Hasło to: " + self.haslo)
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                    else:
                                        wynik = self.pokaz_wiadomosc(f"Gratulacje, hasło odgadnięte poprawnie. \n Liczba prób: {self.rzad} \n Hasło to: " + self.haslo)
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                    return
                                self.proba_teraz = ''
                                if self.rzad >= RZEDY:  # Sprawdza, czy przekroczono liczbę prób.
                                    if tryb == "najwięcej_słów":
                                        self.rzad = 0
                                        self.proby = [[''] * KOLUMNY for _ in range(RZEDY)]
                                        self.kolory = [[BIALY] * KOLUMNY for _ in range(RZEDY)]
                                        self.proba_teraz = ''
                                        self.haslo = random.choice(self.mozliwe_hasla)
                                        continue
                                    else:
                                        wynik = self.pokaz_wiadomosc("Przegrałeś. Hasło to: " + self.haslo)
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                        return
                    elif zdarzenie.unicode.isalpha() and len(self.proba_teraz) < KOLUMNY:
                        self.proba_teraz += zdarzenie.unicode.upper()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:  # Obsługuje kliknięcie przycisku menu.
                    if self.menu_button.collidepoint(zdarzenie.pos):
                        return

            pygame.display.flip()

class Menu:
    """Inicjalizuje okno gry i ustawia jego tytuł."""
    def __init__(self) -> None:
        self.okno: pygame.Surface = pygame.display.set_mode((SZEROKOSC_OKNA, WYSOKOSC_OKNA), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")
        self.tlo = pygame.image.load("tlo.jpeg")
        self.tlo = pygame.transform.scale(self.tlo, (SZEROKOSC_OKNA, WYSOKOSC_OKNA))

    def tekst_w_kracie(self, tekst: str, czcionka: pygame.font.Font, kolor: Tuple[int, int, int], kwadrat: pygame.Rect) -> None:
        """Rysuje tekst na ekranie w podanych kwadracie."""
        tekst_wierzch: pygame.Surface = czcionka.render(tekst, True, kolor)
        tekst_kwadrat: pygame.Rect = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def menu(self) -> None:
        """Wyświetla menu główne i obsługuje wybór trybu gry."""
        game: WordleGame = WordleGame()
        while True:
            self.okno.blit(self.tlo, (0, 0))
            self.tekst_w_kracie("WORDLE", CZCIONKA_DUZA, CZARNY, pygame.Rect(0, 50, SZEROKOSC_OKNA, 100))

            # Zdefiniowanie prostokątów dla przycisków w menu
            standardowy_przycisk: pygame.Rect = pygame.Rect(155, 280, 200, 50)
            najwiecej_slow_przycisk: pygame.Rect = pygame.Rect(155, 380, 200, 50)
            na_czas_przycisk: pygame.Rect = pygame.Rect(155, 480, 200, 50)

            # Rysowanie przycisków na ekranie
            pygame.draw.rect(self.okno, ROZOWY, standardowy_przycisk)
            pygame.draw.rect(self.okno, ROZOWY, najwiecej_slow_przycisk)
            pygame.draw.rect(self.okno, ROZOWY, na_czas_przycisk)

            # Dodanie tekstów na przyciskach
            self.tekst_w_kracie("Standardowa gra", CZCIONKA_MALA, CZARNY, standardowy_przycisk)
            self.tekst_w_kracie("Najwięcej słów", CZCIONKA_MALA, CZARNY, najwiecej_slow_przycisk)
            self.tekst_w_kracie("Gra na czas", CZCIONKA_MALA, CZARNY, na_czas_przycisk)

            pygame.display.flip()

            # Obsługa zdarzeń
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    if standardowy_przycisk.collidepoint(zdarzenie.pos):
                        game.main("standard")
                    elif najwiecej_slow_przycisk.collidepoint(zdarzenie.pos):
                        game.main("najwięcej_słów")
                    elif na_czas_przycisk.collidepoint(zdarzenie.pos):
                        game.main("na_czas")

if __name__ == "__main__":
    Menu().menu()
