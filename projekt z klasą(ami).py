import pygame
import sys
import random
import time

pygame.init()

wysokosc_okna = 650
szerokosc_okna = 510
kolumny = 5
rzedy = 6
rozmiar_okna = 100
brzeg = 5
tlo = (255, 255, 255)

czarny = (0, 0, 0)
szary = (155, 155, 155)
zolty = (255, 212, 34)
zielony = (58, 205, 22)
bialy = (255, 255, 255)
czerwony = (255, 50, 30)

czcionka_duze = pygame.font.SysFont('times new roman', 68)
czcionka_male = pygame.font.SysFont('times new roman', 28)
czcionka_czas = pygame.font.SysFont('times new roman', 28)


class WordleGame:
    def __init__(self):
        self.okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")
        self.mozliwe_hasla = self.lista_hasel()
        self.haslo = random.choice(self.mozliwe_hasla)
        self.proby = [[''] * kolumny for _ in range(rzedy)]
        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
        self.proba_teraz = ''
        self.rzad = 0
        self.start_czas = None
        self.limit_czasu = None
        self.komunikat = None
        self.licznik_slow = 0  

    from listy_slow import lista_hasel
    from listy_slow import lista_slow

    def sprawdzanie(self, proba):
        """Porównuje aktualną próbę gracza z odgadywanym hasłem.
        
        Dla słowa wpisanego przez użytkownika, funkcja zwraca zbiory krotek '(litera, indeks)';
        zielone- poprawne litery na poprawnych pozycjach
        zolte- poprawne litery na niepoprawnych pozycjach
        szare- niepoprawne litery.
        """
        zielone, zolte, szare = set(), set(), set()
        ile_w_hasle = {char: self.haslo.count(char) for char in self.haslo}
        zielone_indeksy = set()

        for i, char in enumerate(self.haslo):
            if char == proba[i]:
                zielone.add((proba[i], i))
                zielone_indeksy.add(i)
                ile_w_hasle[proba[i]] -= 1

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
        for r, próba in enumerate(self.proby):
            for k, litera in enumerate(próba):
                kwadr = pygame.Rect(k * rozmiar_okna + brzeg, r * rozmiar_okna + brzeg, 
                    rozmiar_okna - brzeg, rozmiar_okna - brzeg)
                pygame.draw.rect(self.okno, self.kolory[r][k], kwadr)
                if litera:
                    self.tekst_w_kracie(litera, czcionka_duze, czarny, kwadr)

        for i in range(kolumny):
            kwadr = pygame.Rect(i * rozmiar_okna + brzeg, self.rzad * rozmiar_okna + brzeg,
                rozmiar_okna - brzeg, rozmiar_okna - brzeg)
            pygame.draw.rect(self.okno, bialy, kwadr)
            if i < len(self.proba_teraz):
                self.tekst_w_kracie(self.proba_teraz[i], czcionka_duze, czarny, kwadr)
            pygame.draw.rect(self.okno, czarny, kwadr, 2)

        if pozostaly_czas is not None:
            czas_minuty = pozostaly_czas // 60
            czas_sekundy = pozostaly_czas % 60
            czas_tekst = czcionka_czas.render(f"{czas_minuty}:{czas_sekundy:02}", True, czarny)
            self.okno.blit(czas_tekst, (szerokosc_okna - 100, wysokosc_okna - 40))
            if pozostaly_czas>120:
                licznik_tekst = czcionka_czas.render(f"Słowa: {self.licznik_slow}", True, czarny)
                self.okno.blit(licznik_tekst, (20, wysokosc_okna - 40))
            
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

    def pokaz_wiadomosc(self, wiadomość):
        """Wyświetla wiadomość na ekranie wraz z dwoma przyciskami do wyboru akcji.
        Wyświetla podaną wiadomość na środku ekranu oraz dwa przyciski: "Wróć do menu" i "Zagraj ponownie". 
        Po wybraniu jednej z opcji przez użytkownika  zwraca "menu" lub "ponownie".
        """
        while True:
            self.okno.fill(tlo)
            self.tekst_w_kracie(wiadomość, czcionka_male, czarny,
                pygame.Rect(0, wysokosc_okna // 2 - 50, szerokosc_okna, 100))

            przycisk_menu = pygame.Rect(szerokosc_okna // 2 - 100, wysokosc_okna // 2 + 100, 200, 50)
            przycisk_ponownie = pygame.Rect(szerokosc_okna // 2 - 100, wysokosc_okna // 2 + 170, 200, 50)
        
            pygame.draw.rect(self.okno, zielony, przycisk_menu)
            pygame.draw.rect(self.okno, zolty, przycisk_ponownie)

            self.tekst_w_kracie("Wróć do menu", czcionka_male, czarny, przycisk_menu)
            self.tekst_w_kracie("Zagraj ponownie", czcionka_male, czarny, przycisk_ponownie)

            pygame.display.flip()

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
        self.haslo = random.choice(self.mozliwe_hasla)
        self.proby = [[''] * kolumny for _ in range(rzedy)]
        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
        self.proba_teraz = ''
        self.rzad = 0
        self.start_czas = time.time() if tryb != "standard" else None
        self.limit_czasu = 120 if tryb == "czasowy" else (300 if tryb == "najwięcej_słów" else None)
        self.komunikat = None
        self.komunikat_czas = None
        self.licznik_slow = 0

        while True:
            if tryb != "standard":
                pozostaly_czas = max(0, self.limit_czasu - int(time.time() - self.start_czas))
                if pozostaly_czas <= 0:
                    if tryb == "czasowy":
                        wynik = self.pokaz_wiadomosc("Czas się skończył. Hasło to: " + self.haslo)
                    elif tryb == "najwięcej_słów":
                        wynik = self.pokaz_wiadomosc(f"Czas się skończył. Poprawne słowa: {self.licznik_slow}")
                    if wynik == "ponownie":
                        self.main(tryb)
                    elif wynik == "menu":
                        return
                    return
            else:
                pozostaly_czas = None

            self.krata()
            self.rysuj_tekst(pozostaly_czas)
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.KEYDOWN:
                    if zdarzenie.key == pygame.K_BACKSPACE:
                        self.proba_teraz = self.proba_teraz[:-1]
                    elif zdarzenie.key == pygame.K_RETURN:
                        if len(self.proba_teraz) == kolumny:
                            if self.proba_teraz not in self.lista_slow():
                                self.komunikat = "Słowo niepoprawne"
                                self.komunikat_czas = time.time()
                            else:
                                self.komunikat = None
                                self.komunikat_czas = None
                                zielone, zolte, szare = self.sprawdzanie(self.proba_teraz)
                                for i, litera in enumerate(self.proba_teraz):
                                    if (litera, i) in zielone:
                                        self.kolory[self.rzad][i] = zielony
                                    elif (litera, i) in zolte:
                                        self.kolory[self.rzad][i] = zolty
                                    elif (litera, i) in szare:
                                        self.kolory[self.rzad][i] = szary
                                self.proby[self.rzad] = list(self.proba_teraz)
                                self.rzad += 1
                                if self.proba_teraz == self.haslo:
                                    if tryb == "najwięcej_słów":
                                        self.licznik_slow += 1
                                        self.rzad = 0
                                    
                                        self.proby = [[''] * kolumny for _ in range(rzedy)]
                                        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
                                        self.proba_teraz = ''
                                        self.haslo = random.choice(self.mozliwe_hasla)
                                    else:
                                        wynik = self.pokaz_wiadomosc("Gratulacje, hasło odgadnięte poprawnie")
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                        return
                                self.proba_teraz = ''
                                if self.rzad >= rzedy:
                                    if tryb == "najwięcej_słów":
                                        self.rząd = 0
                                        self.proby = [[''] * kolumny for _ in range(rzedy)]
                                        self.kolory = [[bialy] * kolumny for _ in range(rzedy)]
                                        self.proba_teraz = ''
                                        self.haslo = random.choice(self.mozliwe_hasla)
                                    else:
                                        wynik = self.pokaz_wiadomosc("Przegrałeś. Hasło to: " + self.haslo)
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                        return
                    elif zdarzenie.unicode.isalpha() and len(self.proba_teraz) < kolumny:
                        self.proba_teraz += zdarzenie.unicode.upper()

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

            standardowy_przycisk = pygame.Rect(155, 250, 200, 50)
            czasowy_przycisk = pygame.Rect(155, 350, 200, 50)
            najwiecej_slow_przycisk = pygame.Rect(155, 450, 200, 50)  

            pygame.draw.rect(self.okno, czerwony, standardowy_przycisk)
            pygame.draw.rect(self.okno, czerwony, czasowy_przycisk)
            pygame.draw.rect(self.okno, czerwony, najwiecej_slow_przycisk) 

            self.tekst_w_kracie("Standardowa Gra", czcionka_male, czarny, standardowy_przycisk)
            self.tekst_w_kracie("Gra Na Czas", czcionka_male, czarny, czasowy_przycisk)
            self.tekst_w_kracie("Najwięcej Słów", czcionka_male, czarny, najwiecej_slow_przycisk)  

            pygame.display.flip()

            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    if standardowy_przycisk.collidepoint(zdarzenie.pos):
                        game.main("standard")
                    elif czasowy_przycisk.collidepoint(zdarzenie.pos):
                        game.main("czasowy")
                    elif najwiecej_slow_przycisk.collidepoint(zdarzenie.pos):
                        game.main("najwięcej_słów")  


if __name__ == "__main__":
    Menu().menu()
