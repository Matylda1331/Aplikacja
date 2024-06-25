import unittest
from main_projekt import WordleGame 

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.game = WordleGame()

    def test_wszystko_dobrze(self):
        self.game.haslo = "CLOUD"
        proba = "CLOUD"
        zielone, zolte, szare = self.game.sprawdzanie(proba)
        self.assertEqual(len(zielone), 5)
        self.assertEqual(len(zolte), 0)
        self.assertEqual(len(szare), 0)
        self.assertIn(('C', 0), zielone)
        self.assertIn(('L', 1), zielone)
        self.assertIn(('O', 2), zielone)
        self.assertIn(('U', 3), zielone)
        self.assertIn(('D', 4), zielone)
    
    def test_zla_litera(self):
        self.game.haslo = "APPLE"
        proba = "APPLY"
        zielone, zolte, szare = self.game.sprawdzanie(proba)
        self.assertEqual(len(zielone), 4)
        self.assertEqual(len(zolte), 0)
        self.assertEqual(len(szare), 1)
        self.assertIn(('A', 0), zielone)
        self.assertIn(('P', 1), zielone)
        self.assertIn(('P', 2), zielone)
        self.assertIn(('L', 3), zielone)
        self.assertIn(('Y', 4), szare)    
    
    def test_brak_zielonych(self):
        self.game.haslo = "APPLE"
        proba = "PINKY"
        zielone, zolte, szare = self.game.sprawdzanie(proba)
        self.assertEqual(len(zielone), 0)
        self.assertEqual(len(zolte), 1)
        self.assertEqual(len(szare), 4)
        self.assertIn(('P', 0), zolte)
        self.assertIn(('I', 1), szare)
        self.assertIn(('N', 2), szare)
        self.assertIn(('K', 3), szare)
        self.assertIn(('Y', 4), szare)
    

if __name__ == "__main__":
    unittest.main()
