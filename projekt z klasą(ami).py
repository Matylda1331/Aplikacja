import pygame
import sys
import random
import time

pygame.init()

# Ustawienia okna gry
wysokosc_okna = 650
szerokosc_okna = 510
kolumny = 5
rzedy = 6
rozmiar_okna = 100
brzeg = 5
tlo = (255, 255, 255)

# Kolory używane w grze
czarny = (0, 0, 0)
szary = (155, 155, 155)
zolty = (255, 212, 34)
zielony = (58, 205, 22)
bialy = (255, 255, 255)
czerwony = (255, 50, 30)

# Czcionki używane w grze
czcionka_duze = pygame.font.SysFont('times new roman', 68)
czcionka_male = pygame.font.SysFont('times new roman', 28)
czcionka_czas = pygame.font.SysFont('times new roman', 28)


class WordleGame:
    def __init__(self):
        # Inicjalizacja okna gry
        self.okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")
        self.mozliwe_hasla = self.lista_hasel()
        self.haslo = random.choice(self.mozliwe_hasla) # Losowe hasło
        self.proby = [[''] * kolumny for _ in range(rzedy)]
        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
        self.proba_teraz = ''
        self.rzad = 0
        self.start_czas = None
        self.limit_czasu = None
        self.komunikat = None
        self.licznik_slow = 0  

    from listy_slow import lista_hasel # Import listy haseł
    from listy_slow import lista_slow # Import listy słów

    def sprawdzanie(self, proba):
        """Porównuje aktualną próbę gracza z odgadywanym hasłem.
        
        Dla słowa wpisanego przez użytkownika, funkcja zwraca zbiory krotek '(litera, indeks)';
        zielone- poprawne litery na poprawnych pozycjach
        zolte- poprawne litery na niepoprawnych pozycjach
        szare- niepoprawne litery.
        """
        zielone, zolte, szare = set(), set(), set()
        ile_w_hasle = {char: self.haslo.count(char) for char in self.haslo} # Ile każdej litery w haśle
        zielone_indeksy = set()

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
    
    def krata(self):
        """Rysuje kratę do gry."""
        self.okno.fill(tlo)
        for rzad in range(rzedy):
            for kolumna in range(kolumny):
                kwadraty = pygame.Rect(kolumna * rozmiar_okna + brzeg, rzad * rozmiar_okna + brzeg,
                    rozmiar_okna - brzeg,rozmiar_okna - brzeg)
                pygame.draw.rect(self.okno, czarny, kwadraty, 2)

    def tekst_w_kracie(self, tekst, czcionka, kolor, kwadrat):
        """Rysuje litery."""
        tekst_wierzch = czcionka.render(tekst, True, kolor)
        tekst_kwadrat = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def rysuj_tekst(self, pozostaly_czas=None):
        """Rysuje elementy interfejsu na ekranie gry: kratę do gry, wprowadzone słowa, 
        litery wpisywane w bieżącej próbie, a w przypadku podania argumentu pozostaly_czas odliczanie czasu
        i liczbę odgadniętych słów.
        """
        # Rysowanie wprowadzonych słów
        for r, próba in enumerate(self.proby):
            for k, litera in enumerate(próba):
                kwadr = pygame.Rect(k * rozmiar_okna + brzeg, r * rozmiar_okna + brzeg, 
                    rozmiar_okna - brzeg, rozmiar_okna - brzeg)
                pygame.draw.rect(self.okno, self.kolory[r][k], kwadr)
                if litera:
                    self.tekst_w_kracie(litera, czcionka_duze, czarny, kwadr)

        # Rysowanie bieżącej próby
        for i in range(kolumny):
            kwadr = pygame.Rect(i * rozmiar_okna + brzeg, self.rzad * rozmiar_okna + brzeg,
                rozmiar_okna - brzeg, rozmiar_okna - brzeg)
            pygame.draw.rect(self.okno, bialy, kwadr)
            if i < len(self.proba_teraz):
                self.tekst_w_kracie(self.proba_teraz[i], czcionka_duze, czarny, kwadr)
            pygame.draw.rect(self.okno, czarny, kwadr, 2)

        # Rysowanie odliczania czasu i licznika słów
        if pozostaly_czas is not None:
            czas_minuty = pozostaly_czas // 60
            czas_sekundy = pozostaly_czas % 60
            czas_tekst = czcionka_czas.render(f"{czas_minuty}:{czas_sekundy:02}", True, czarny)
            self.okno.blit(czas_tekst, (szerokosc_okna - 100, wysokosc_okna - 40))
            licznik_tekst = czcionka_czas.render(f"Słowa: {self.licznik_slow}", True, czarny)
            self.okno.blit(licznik_tekst, (20, wysokosc_okna - 40))

        # Aktualizacja czasu gry
        czas = self.aktualizuj_czas()
        if czas is not None:
            czas_tekst = czcionka_czas.render(czas, True, czarny)
            self.okno.blit(czas_tekst, (20, wysokosc_okna - 40))

        # Wyświetlanie błędu 
        if self.komunikat is not None and self.komunikat_czas is not None:
            if time.time() - self.komunikat_czas < 1.2:
                komunikat_prostokat = pygame.Rect(55, 220, 400, 50)
                pygame.draw.rect(self.okno, czerwony, komunikat_prostokat)
                komunikat_tekst = czcionka_male.render(self.komunikat, True, czarny)
                komunikat_rect = komunikat_tekst.get_rect(center=komunikat_prostokat.center)
                self.okno.blit(komunikat_tekst, komunikat_rect)
            else:
                self.komunikat = None
                self.komunikat_czas = None

        #Dodanie przycisku MENU
        self.menu_button = pygame.Rect(szerokosc_okna // 2 - 50, wysokosc_okna - 37, 100, 30)
        pygame.draw.rect(self.okno, szary, self.menu_button)
        self.tekst_w_kracie("MENU", czcionka_male, czarny, self.menu_button)

    def aktualizuj_czas(self):
        if self.start_czas is not None and self.tryb == "na_czas":
            ile_czasu = int(time.time() - self.start_czas) # Oblicza upływający czas od startu gry
            czas_minuty = ile_czasu // 60
            czas_sekundy = ile_czasu % 60
            return f"{czas_minuty}:{czas_sekundy:02}" # Formatuje czas jako "MM:SS".
        return None

    def pokaz_wiadomosc(self, wiadomosc):
        """Wyświetla wiadomość na ekranie wraz z dwoma przyciskami do wyboru akcji.
        Wyświetla podaną wiadomość na środku ekranu oraz dwa przyciski: "Wróć do menu" i "Zagraj ponownie". 
        Po wybraniu jednej z opcji przez użytkownika  zwraca "menu" lub "ponownie".
        """
        while True:
            self.okno.fill(tlo)
            linie_wiadomosci = wiadomosc.split('\n')
            y = wysokosc_okna // 2 - 50
            for linia in linie_wiadomosci:
                self.tekst_w_kracie(linia, czcionka_male, czarny, pygame.Rect(0, y, szerokosc_okna, 50))
                y += 50

            #Dodanie przycisków 
            przycisk_menu = pygame.Rect(szerokosc_okna // 2 - 100, wysokosc_okna // 2 + 100, 200, 50)
            przycisk_ponownie = pygame.Rect(szerokosc_okna // 2 - 100, wysokosc_okna // 2 + 170, 200, 50)
        
            pygame.draw.rect(self.okno, zielony, przycisk_menu)
            pygame.draw.rect(self.okno, zolty, przycisk_ponownie)

            self.tekst_w_kracie("Wróć do menu", czcionka_male, czarny, przycisk_menu)
            self.tekst_w_kracie("Zagraj ponownie", czcionka_male, czarny, przycisk_ponownie)

            pygame.display.flip()

            #Dodanie działania przycisków 
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    if przycisk_menu.collidepoint(zdarzenie.pos):
                        return "menu"
                    elif przycisk_ponownie.collidepoint(zdarzenie.pos):
                        return "ponownie"

    def main(self, tryb):
        """Główna funkcja gry. W zależności od trybu inicjalizuje ustawienia gry,
        rysuje interfejs, obsługuje zdarzenia PyGame"""
        self.tryb = tryb
        self.haslo = random.choice(self.mozliwe_hasla)
        self.proby = [[''] * kolumny for _ in range(rzedy)]
        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
        self.proba_teraz = ''
        self.rzad = 0
        self.start_czas = time.time() if tryb != "standard" else None
        self.limit_czasu = 300 if tryb == "najwięcej_słów" else None #Ustawienie czasu w trybie najwięcej słów
        self.komunikat = None
        self.komunikat_czas = None
        self.licznik_slow = 0

        while True:
            # Sprawdza pozostały czas
            if tryb != "standard" and tryb != "na_czas":
                pozostaly_czas = max(0, self.limit_czasu - int(time.time() - self.start_czas))
                if pozostaly_czas <= 0:
                    if wynik == "ponownie":
                        self.main(tryb)
                    elif tryb == "najwięcej_słów":
                        wynik = self.pokaz_wiadomosc(f"Czas się skończył. Poprawne słowa: {self.licznik_slow}")
                    elif wynik == "menu":
                        return
                    return
            else:
                pozostaly_czas = None

            self.krata() # Rysuje planszę gry.
            self.rysuj_tekst(pozostaly_czas) # Rysuje pozostały czas.

            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT: # Sprawdza, czy użytkownik zamknął okno.
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.KEYDOWN:
                    if zdarzenie.key == pygame.K_BACKSPACE:
                        self.proba_teraz = self.proba_teraz[:-1]
                    elif zdarzenie.key == pygame.K_RETURN:
                        if len(self.proba_teraz) == kolumny: # Sprawdza, czy długość słowa jest zgodna.
                            if self.proba_teraz not in self.lista_slow(): # Sprawdza poprawność słowa.
                                self.komunikat = "Słowo niepoprawne"
                                self.komunikat_czas = time.time()
                            else:
                                self.komunikat = None
                                self.komunikat_czas = None
                                zielone, zolte, szare = self.sprawdzanie(self.proba_teraz) # Sprawdza poprawność liter.
                                for i, litera in enumerate(self.proba_teraz):
                                    if (litera, i) in zielone:
                                        self.kolory[self.rzad][i] = zielony
                                    elif (litera, i) in zolte:
                                        self.kolory[self.rzad][i] = zolty
                                    elif (litera, i) in szare:
                                        self.kolory[self.rzad][i] = szary
                                self.proby[self.rzad] = list(self.proba_teraz)
                                self.rzad += 1
                                if self.proba_teraz == self.haslo: # Sprawdza, czy słowo jest poprawne.
                                    if tryb == "najwięcej_słów":
                                        self.licznik_slow += 1
                                        self.rzad = 0
                                        self.proby = [[''] * kolumny for _ in range(rzedy)]
                                        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
                                        self.proba_teraz = ''
                                        self.haslo = random.choice(self.mozliwe_hasla)
                                        continue
                                    elif tryb == "na_czas":
                                        ile_czasu = int(time.time() - self.start_czas)
                                        wynik = self.pokaz_wiadomosc(f"Gratulacje, hasło odgadnięte poprawnie. \n Czas: {ile_czasu // 60}:{ile_czasu % 60:02}")
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                    else:
                                        wynik = self.pokaz_wiadomosc("Gratulacje, hasło odgadnięte poprawnie")
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                    return
                                self.proba_teraz = ''
                                if self.rzad >= rzedy: # Sprawdza, czy przekroczono liczbę prób.
                                    if tryb == "najwięcej_słów":
                                        self.rząd = 0
                                        self.proby = [[''] * kolumny for _ in range(rzedy)]
                                        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
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
                    elif zdarzenie.unicode.isalpha() and len(self.proba_teraz) < kolumny:
                        self.proba_teraz += zdarzenie.unicode.upper()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN: # Obsługuje kliknięcie przycisku menu.
                    if self.menu_button.collidepoint(zdarzenie.pos):
                        return

            pygame.display.flip()


class Menu:
    """Inicjalizuje okno gry i ustawia jego tytuł."""
    def __init__(self):
        self.okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")

    def tekst_w_kracie(self, tekst, czcionka, kolor, kwadrat):
        """Rysuje tekst na ekranie w podanych kwadracie."""
        tekst_wierzch = czcionka.render(tekst, True, kolor)
        tekst_kwadrat = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def menu(self):
        """Wyświetla menu główne i obsługuje wybór trybu gry."""
        game = WordleGame()
        while True:
            self.okno.fill(tlo)
            self.tekst_w_kracie("WORDLE", czcionka_duze, czarny, pygame.Rect(0, 50, szerokosc_okna, 100))

            # Zdefiniowanie prostokątów dla przycisków w menu
            standardowy_przycisk = pygame.Rect(155, 280, 200, 50)
            najwiecej_slow_przycisk = pygame.Rect(155, 380, 200, 50)  
            na_czas_przycisk = pygame.Rect(155, 480, 200, 50)

            # Rysowanie przycisków na ekranie
            pygame.draw.rect(self.okno, czerwony, standardowy_przycisk)
            pygame.draw.rect(self.okno, czerwony, najwiecej_slow_przycisk) 
            pygame.draw.rect(self.okno, czerwony, na_czas_przycisk)

            # Dodanie tekstów na przyciskach
            self.tekst_w_kracie("Standardowa gra", czcionka_male, czarny, standardowy_przycisk)
            self.tekst_w_kracie("Najwięcej słów", czcionka_male, czarny, najwiecej_slow_przycisk)
            self.tekst_w_kracie("Gra na czas", czcionka_male, czarny, na_czas_przycisk) 

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
