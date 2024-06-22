import pygame
import sys
import random
import time

pygame.init()

wysokość_okna = 650
szerokość_okna = 510
kolumny = 5
rzędy = 6
rozmiar_okna = 100
brzeg = 5
tło = (255, 255, 255)

czarny = (0, 0, 0)
szary = (155, 155, 155)
żółty = (255, 212, 34)
zielony = (58, 205, 22)
biały = (255, 255, 255)
czerwony = (255, 50, 30)

czcionka_duże = pygame.font.SysFont('times new roman', 68)
czcionka_małe = pygame.font.SysFont('times new roman', 28)
czcionka_czas = pygame.font.SysFont('times new roman', 28)


class WordleGame:
    def __init__(self):
        self.okno = pygame.display.set_mode((szerokość_okna, wysokość_okna), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")
        self.możliwe_hasła = self.lista_haseł()
        self.hasło = random.choice(self.możliwe_hasła)
        self.próby = [[''] * kolumny for _ in range(rzędy)]
        self.kolory = [[biały] * kolumny for _ in range(rzędy)]
        self.próba_teraz = ''
        self.rząd = 0
        self.start_czas = None
        self.limit_czasu = None
        self.komunikat = None
        self.licznik_slow = 0  
    from listy_slow import lista_haseł
    from listy_slow import lista_słów
    def sprawdzanie(self, próba):
        zielone, zolte, szare = set(), set(), set()
        ile_w_haśle = {char: self.hasło.count(char) for char in self.hasło}
        zielone_indeksy = set()

        for i, char in enumerate(self.hasło):
            if char == próba[i]:
                zielone.add((próba[i], i))
                zielone_indeksy.add(i)
                ile_w_haśle[próba[i]] -= 1

        for i, char in enumerate(próba):
            if i not in zielone_indeksy:
                if char in self.hasło and ile_w_haśle.get(char, 0) > 0:
                    zolte.add((char, i))
                    ile_w_haśle[char] -= 1
                else:
                    szare.add((char, i))

        return zielone, zolte, szare

    def krata(self):
        self.okno.fill(tło)
        for rzad in range(rzędy):
            for kolumna in range(kolumny):
                kwadraty = pygame.Rect(kolumna * rozmiar_okna + brzeg, rzad * rozmiar_okna + brzeg, rozmiar_okna - brzeg, rozmiar_okna - brzeg)
                pygame.draw.rect(self.okno, czarny, kwadraty, 2)

    def tekst_w_kracie(self, tekst, czcionka, kolor, kwadrat):
        tekst_wierzch = czcionka.render(tekst, True, kolor)
        tekst_kwadrat = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def rysuj_tekst(self, pozostały_czas=None):
        for r, próba in enumerate(self.próby):
            for k, litera in enumerate(próba):
                kwadr = pygame.Rect(k * rozmiar_okna + brzeg, r * rozmiar_okna + brzeg, rozmiar_okna - brzeg, rozmiar_okna - brzeg)
                pygame.draw.rect(self.okno, self.kolory[r][k], kwadr)
                if litera:
                    self.tekst_w_kracie(litera, czcionka_duże, czarny, kwadr)

        for i in range(kolumny):
            kwadr = pygame.Rect(i * rozmiar_okna + brzeg, self.rząd * rozmiar_okna + brzeg, rozmiar_okna - brzeg, rozmiar_okna - brzeg)
            pygame.draw.rect(self.okno, biały, kwadr)
            if i < len(self.próba_teraz):
                self.tekst_w_kracie(self.próba_teraz[i], czcionka_duże, czarny, kwadr)
            pygame.draw.rect(self.okno, czarny, kwadr, 2)

        if pozostały_czas is not None:
            czas_minuty = pozostały_czas // 60
            czas_sekundy = pozostały_czas % 60
            czas_tekst = czcionka_czas.render(f"{czas_minuty}:{czas_sekundy:02}", True, czarny)
            self.okno.blit(czas_tekst, (szerokość_okna - 100, wysokość_okna - 40))
            if pozostały_czas>120:
                licznik_tekst = czcionka_czas.render(f"Słowa: {self.licznik_slow}", True, czarny)
                self.okno.blit(licznik_tekst, (20, wysokość_okna - 40))
            

        if self.komunikat is not None and self.komunikat_czas is not None:
            if time.time() - self.komunikat_czas < 1.2:
                komunikat_prostokąt = pygame.Rect(55, 220, 400, 50)
                pygame.draw.rect(self.okno, czerwony, komunikat_prostokąt)
                komunikat_tekst = czcionka_małe.render(self.komunikat, True, czarny)
                komunikat_rect = komunikat_tekst.get_rect(center=komunikat_prostokąt.center)
                self.okno.blit(komunikat_tekst, komunikat_rect)
            else:
                self.komunikat = None
                self.komunikat_czas = None

    def pokaz_wiadomość(self, wiadomość):
        while True:
            self.okno.fill(tło)
            self.tekst_w_kracie(wiadomość, czcionka_małe, czarny, pygame.Rect(0, wysokość_okna // 2 - 50, szerokość_okna, 100))

            przycisk_menu = pygame.Rect(szerokość_okna // 2 - 100, wysokość_okna // 2 + 100, 200, 50)
            przycisk_ponownie = pygame.Rect(szerokość_okna // 2 - 100, wysokość_okna // 2 + 170, 200, 50)
        
            pygame.draw.rect(self.okno, zielony, przycisk_menu)
            pygame.draw.rect(self.okno, żółty, przycisk_ponownie)

            self.tekst_w_kracie("Wróć do menu", czcionka_małe, czarny, przycisk_menu)
            self.tekst_w_kracie("Zagraj ponownie", czcionka_małe, czarny, przycisk_ponownie)

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
        self.hasło = random.choice(self.możliwe_hasła)
        self.próby = [[''] * kolumny for _ in range(rzędy)]
        self.kolory = [[biały] * kolumny for _ in range(rzędy)]
        self.próba_teraz = ''
        self.rząd = 0
        self.start_czas = time.time() if tryb != "standard" else None
        self.limit_czasu = 120 if tryb == "czasowy" else (300 if tryb == "najwięcej_słów" else None)
        self.komunikat = None
        self.komunikat_czas = None
        self.licznik_slow = 0

        while True:
            if tryb != "standard":
                pozostały_czas = max(0, self.limit_czasu - int(time.time() - self.start_czas))
                if pozostały_czas <= 0:
                    if tryb == "czasowy":
                        wynik = self.pokaz_wiadomość("Czas się skończył. Hasło to: " + self.hasło)
                    elif tryb == "najwięcej_słów":
                        wynik = self.pokaz_wiadomość(f"Czas się skończył. Poprawne słowa: {self.licznik_slow}")
                    if wynik == "ponownie":
                        self.main(tryb)
                    elif wynik == "menu":
                        return
                    return
            else:
                pozostały_czas = None

            self.krata()
            self.rysuj_tekst(pozostały_czas)

            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.KEYDOWN:
                    if zdarzenie.key == pygame.K_BACKSPACE:
                        self.próba_teraz = self.próba_teraz[:-1]
                    elif zdarzenie.key == pygame.K_RETURN:
                        if len(self.próba_teraz) == kolumny:
                            if self.próba_teraz not in self.lista_słów():
                                self.komunikat = "Słowo niepoprawne"
                                self.komunikat_czas = time.time()
                            else:
                                self.komunikat = None
                                self.komunikat_czas = None
                                zielone, zolte, szare = self.sprawdzanie(self.próba_teraz)
                                for i, litera in enumerate(self.próba_teraz):
                                    if (litera, i) in zielone:
                                        self.kolory[self.rząd][i] = zielony
                                    elif (litera, i) in zolte:
                                        self.kolory[self.rząd][i] = żółty
                                    elif (litera, i) in szare:
                                        self.kolory[self.rząd][i] = szary
                                self.próby[self.rząd] = list(self.próba_teraz)
                                self.rząd += 1
                                if self.próba_teraz == self.hasło:
                                    if tryb == "najwięcej_słów":
                                        self.licznik_slow += 1
                                        self.rząd = 0
                                    
                                        self.próby = [[''] * kolumny for _ in range(rzędy)]
                                        self.kolory = [[biały] * kolumny for _ in range(rzędy)]
                                        self.próba_teraz = ''
                                        self.hasło = random.choice(self.możliwe_hasła)
                                    else:
                                        wynik = self.pokaz_wiadomość("Gratulacje, hasło odgadnięte poprawnie")
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                        return
                                self.próba_teraz = ''
                                if self.rząd >= rzędy:
                                    if tryb == "najwięcej_słów":
                                        self.rząd = 0
                                        self.próby = [[''] * kolumny for _ in range(rzędy)]
                                        self.kolory = [[biały] * kolumny for _ in range(rzędy)]
                                        self.próba_teraz = ''
                                        self.hasło = random.choice(self.możliwe_hasła)
                                    else:
                                        wynik = self.pokaz_wiadomość("Przegrałeś. Hasło to: " + self.hasło)
                                        if wynik == "ponownie":
                                            self.main(tryb)
                                        elif wynik == "menu":
                                            return
                                        return
                    elif zdarzenie.unicode.isalpha() and len(self.próba_teraz) < kolumny:
                        self.próba_teraz += zdarzenie.unicode.upper()

            pygame.display.flip()



class Menu:
    def __init__(self):
        self.okno = pygame.display.set_mode((szerokość_okna, wysokość_okna), 0, 32)
        pygame.display.set_caption("WORDLE - Projekt")

    def tekst_w_kracie(self, tekst, czcionka, kolor, kwadrat):
        tekst_wierzch = czcionka.render(tekst, True, kolor)
        tekst_kwadrat = tekst_wierzch.get_rect(center=kwadrat.center)
        self.okno.blit(tekst_wierzch, tekst_kwadrat)

    def menu(self):
        game = WordleGame()
        while True:
            self.okno.fill(tło)
            self.tekst_w_kracie("WORDLE", czcionka_duże, czarny, pygame.Rect(0, 50, szerokość_okna, 100))

            standardowy_przycisk = pygame.Rect(155, 250, 200, 50)
            czasowy_przycisk = pygame.Rect(155, 350, 200, 50)
            najwięcej_słów_przycisk = pygame.Rect(155, 450, 200, 50)  

            pygame.draw.rect(self.okno, czerwony, standardowy_przycisk)
            pygame.draw.rect(self.okno, czerwony, czasowy_przycisk)
            pygame.draw.rect(self.okno, czerwony, najwięcej_słów_przycisk) 

            self.tekst_w_kracie("Standardowa Gra", czcionka_małe, czarny, standardowy_przycisk)
            self.tekst_w_kracie("Gra Na Czas", czcionka_małe, czarny, czasowy_przycisk)
            self.tekst_w_kracie("Najwięcej Słów", czcionka_małe, czarny, najwięcej_słów_przycisk)  

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
                    elif najwięcej_słów_przycisk.collidepoint(zdarzenie.pos):
                        game.main("najwięcej_słów")  


if __name__ == "__main__":
    Menu().menu()

