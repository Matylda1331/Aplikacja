import unittest
from main_projekt import WordleGame 

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.game = WordleGame()

    def test_wszystko_dobrze(self):
        self.game.haslo = "APPLE"
        proba = "APPLE"
        zielone, zolte, szare = self.game.sprawdzanie(proba)
        self.assertEqual(len(zielone), 5)
        self.assertEqual(len(zolte), 0)
        self.assertEqual(len(szare), 0)
        self.assertIn(('A', 0), zielone)
        self.assertIn(('P', 1), zielone)
        self.assertIn(('P', 2), zielone)
        self.assertIn(('L', 3), zielone)
        self.assertIn(('E', 4), zielone)
    
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
        proba = "PALMS"
        zielone, zolte, szare = self.game.sprawdzanie(proba)
        self.assertEqual(len(zielone), 0)
        self.assertEqual(len(zolte), 3)
        self.assertEqual(len(szare), 2)
        self.assertIn(('A', 1), zolte)
        self.assertIn(('P', 0), zolte)
        self.assertIn(('L', 2), zolte)
        self.assertIn(('M', 3), szare)
        self.assertIn(('S', 4), szare)
    

if __name__ == "__main__":
    unittest.main()
