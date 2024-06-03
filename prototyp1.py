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
tło = (255,255,255)

czarny = (0,0,0)
szary = (155,155,155)
żółty = (255,212,34)
zielony = (58,205,22)
biały = (255,255,255)
czerwony = (255, 50, 30)

czcionka_duże = pygame.font.SysFont('times new roman', 68)
czcionka_małe = pygame.font.SysFont('times new roman', 28)
czcionka_czas = pygame.font.SysFont('times new roman', 28)

def sprawdzanie(hasło, próba):
    zielone = set()
    zolte = set()
    szare = set()

    ile_w_haśle = {}
    for char in hasło:
        ile_w_haśle[char] = ile_w_haśle.get(char, 0) + 1

    zielone_indeksy = set()
    for i in range(len(hasło)):
        if hasło[i] == próba[i]:
            zielone.add((próba[i],i))
            zielone_indeksy.add(i)
            ile_w_haśle[próba[i]] -= 1

    for i in range(len(próba)):
        if i not in zielone_indeksy:
            if próba[i] in hasło and ile_w_haśle.get(próba[i], 0) > 0:
                zolte.add((próba[i],i))
                ile_w_haśle[próba[i]] -= 1
            else:
                szare.add((próba[i],i))

    #print("Litery na poprawnym miejscu: " + str(zielone) + ", litery na złym miejscu: " + str(zolte) + ", litery niepoprawne: " + str(szare))
    return zielone, zolte, szare


okno = pygame.display.set_mode((szerokość_okna,wysokość_okna), 0, 32)
pygame.display.set_caption("WORDLE - Projekt")

def krata():
    okno.fill(tło)
    for rzad in range(rzędy):
        for kolumna in range(kolumny):
            kwadraty = pygame.Rect(kolumna*rozmiar_okna+brzeg, rzad*rozmiar_okna+brzeg,rozmiar_okna-brzeg,rozmiar_okna-brzeg)
            pygame.draw.rect(okno, czarny, kwadraty, 2)

def tekst_w_kracie(tekst, czcionka, kolor, kwadrat):
    tekst_wierzch = czcionka.render(tekst, True, kolor)
    tekst_kwadrat = tekst_wierzch.get_rect(center = kwadrat.center)
    okno.blit(tekst_wierzch, tekst_kwadrat)

def rysuj_tekst(próby, kolory, wpisywane, rząd, czas=None):
    for r in range(len(próby)):
        for k in range(len(próby[r])):
            kwadr = pygame.Rect(k * rozmiar_okna + brzeg, r * rozmiar_okna + brzeg, rozmiar_okna - brzeg, rozmiar_okna - brzeg)
            pygame.draw.rect(okno, kolory[r][k], kwadr)
            if próby[r][k]:
                tekst_w_kracie(próby[r][k], czcionka_duże, czarny, kwadr)

    for i in range(kolumny):
        kwadr = pygame.Rect(i * rozmiar_okna + brzeg, rząd * rozmiar_okna + brzeg, rozmiar_okna - brzeg, rozmiar_okna - brzeg)
        pygame.draw.rect(okno, biały, kwadr)
        if i < len(wpisywane):
            tekst_w_kracie(wpisywane[i], czcionka_duże, czarny, kwadr)
        pygame.draw.rect(okno, czarny, kwadr, 2)
    
    if czas is not None:
        czas_minuty = czas // 60
        czas_sekundy = czas % 60
        czas_tekst = czcionka_czas.render(f"{czas_minuty}:{czas_sekundy:02}", True, czarny)
        okno.blit(czas_tekst, (szerokość_okna - 100, wysokość_okna - 40))

def lista_haseł():
    możliwe_hasła = ['ABACK', 'ABASE', 'ABATE', 'ABBEY', 'ABBOT', 'ABHOR', 'ABIDE', 'ABLED', 'ABODE', 'ABORT', 'ABOUT', 'ABOVE', 'ABUSE', 'ABYSS', 'ACORN', 'ACRID', 'ACTOR', 'ACUTE', 'ADAGE', 'ADAPT', 'ADEPT', 'ADMIN', 'ADMIT', 'ADOBE', 'ADOPT', 'ADORE', 'ADORN', 'ADULT', 'AFFIX', 'AFIRE', 'AFOOT', 'AFOUL', 'AFTER', 'AGAIN', 'AGAPE', 'AGATE', 'AGENT', 'AGILE', 'AGING', 'AGLOW', 'AGONY', 'AGORA', 'AGREE', 'AHEAD', 'AIDER', 'AISLE', 'ALARM', 'ALBUM', 'ALERT', 'ALGAE', 'ALIBI', 'ALIEN', 'ALIGN', 'ALIKE', 'ALIVE', 'ALLAY', 'ALLEY', 'ALLOT', 'ALLOW', 'ALLOY', 'ALOFT', 'ALONE', 'ALONG', 'ALOOF', 'ALOUD', 'ALPHA', 'ALTAR', 'ALTER', 'AMASS', 'AMAZE', 'AMBER', 'AMBLE', 'AMEND', 'AMISS', 'AMITY', 'AMONG', 'AMPLE', 'AMPLY', 'AMUSE', 'ANGEL', 'ANGER', 'ANGLE', 'ANGRY', 'ANGST', 'ANIME', 'ANKLE', 'ANNEX', 'ANNOY', 'ANNUL', 'ANODE', 'ANTIC', 'ANVIL', 'AORTA', 'APART', 'APHID', 'APING', 'APNEA', 'APPLE', 'APPLY', 'APRON', 'APTLY', 'ARBOR', 'ARDOR', 'ARENA', 'ARGUE', 'ARISE', 'ARMOR', 'AROMA', 'AROSE', 'ARRAY', 'ARROW', 'ARSON', 'ARTSY', 'ASCOT', 'ASHEN', 'ASIDE', 'ASKEW', 'ASSAY', 'ASSET', 'ATOLL', 'ATONE', 'ATTIC', 'AUDIO', 'AUDIT', 'AUGUR', 'AUNTY', 'AVAIL', 'AVERT', 'AVIAN', 'AVOID', 'AWAIT', 'AWAKE', 'AWARD', 'AWARE', 'AWASH', 'AWFUL', 'AWOKE', 'AXIAL', 'AXIOM', 'AXION', 'AZURE', 'BACON', 'BADGE', 'BADLY', 'BAGEL', 'BAGGY', 'BAKER', 'BALER', 'BALMY', 'BANAL', 'BANJO', 'BARGE', 'BARON', 'BASAL', 'BASIC', 'BASIL', 'BASIN', 'BASIS', 'BASTE', 'BATCH', 'BATHE', 'BATON', 'BATTY', 'BAWDY', 'BAYOU', 'BEACH', 'BEADY', 'BEARD', 'BEAST', 'BEECH', 'BEEFY', 'BEFIT', 'BEGAN', 'BEGAT', 'BEGET', 'BEGIN', 'BEGUN', 'BEING', 'BELCH', 'BELIE', 'BELLE', 'BELLY', 'BELOW', 'BENCH', 'BERET', 'BERRY', 'BERTH', 'BESET', 'BETEL', 'BEVEL', 'BEZEL', 'BIBLE', 'BICEP', 'BIDDY', 'BIGOT', 'BILGE', 'BILLY', 'BINGE', 'BINGO', 'BIOME', 'BIRCH', 'BIRTH', 'BISON', 'BITTY', 'BLACK', 'BLADE', 'BLAME', 'BLAND', 'BLANK', 'BLARE', 'BLAST', 'BLAZE', 'BLEAK', 'BLEAT', 'BLEED', 'BLEEP', 'BLEND', 'BLESS', 'BLIMP', 'BLIND', 'BLINK', 'BLISS', 'BLITZ', 'BLOAT', 'BLOCK', 'BLOKE', 'BLOND', 'BLOOD', 'BLOOM', 'BLOWN', 'BLUER', 'BLUFF', 'BLUNT', 'BLURB', 'BLURT', 'BLUSH', 'BOARD', 'BOAST', 'BOBBY', 'BONEY', 'BONGO', 'BONUS', 'BOOBY', 'BOOST', 'BOOTH', 'BOOTY', 'BOOZE', 'BOOZY', 'BORAX', 'BORNE', 'BOSOM', 'BOSSY', 'BOTCH', 'BOUGH', 'BOULE', 'BOUND', 'BOWEL', 'BOXER', 'BRACE', 'BRAID', 'BRAIN', 'BRAKE', 'BRAND', 'BRASH', 'BRASS', 'BRAVE', 'BRAVO', 'BRAWL', 'BRAWN', 'BREAD', 'BREAK', 'BREED', 'BRIAR', 'BRIBE', 'BRICK', 'BRIDE', 'BRIEF', 'BRINE', 'BRING', 'BRINK', 'BRINY', 'BRISK', 'BROAD', 'BROIL', 'BROKE', 'BROOD', 'BROOK', 'BROOM', 'BROTH', 'BROWN', 'BRUNT', 'BRUSH', 'BRUTE', 'BUDDY', 'BUDGE', 'BUGGY', 'BUGLE', 'BUILD', 'BUILT', 'BULGE', 'BULKY', 'BULLY', 'BUNCH', 'BUNNY', 'BURLY', 'BURNT', 'BURST', 'BUSED', 'BUSHY', 'BUTCH', 'BUTTE', 'BUXOM', 'BUYER', 'BYLAW', 'CABAL', 'CABBY', 'CABIN', 'CABLE', 'CACAO', 'CACHE', 'CACTI', 'CADDY', 'CADET', 'CAGEY', 'CAIRN', 'CAMEL', 'CAMEO', 'CANAL', 'CANDY', 'CANNY', 'CANOE', 'CANON', 'CAPER', 'CAPUT', 'CARAT', 'CARGO', 'CAROL', 'CARRY', 'CARVE', 'CASTE', 'CATCH', 'CATER', 'CATTY', 'CAULK', 'CAUSE', 'CAVIL', 'CEASE', 'CEDAR', 'CELLO', 'CHAFE', 'CHAFF', 'CHAIN', 'CHAIR', 'CHALK', 'CHAMP', 'CHANT', 'CHAOS', 'CHARD', 'CHARM', 'CHART', 'CHASE', 'CHASM', 'CHEAP', 'CHEAT', 'CHECK', 'CHEEK', 'CHEER', 'CHESS', 'CHEST', 'CHICK', 'CHIDE', 'CHIEF', 'CHILD', 'CHILI', 'CHILL', 'CHIME', 'CHINA', 'CHIRP', 'CHOCK', 'CHOIR', 'CHOKE', 'CHORD', 'CHORE', 'CHOSE', 'CHUCK', 'CHUMP', 'CHUNK', 'CHURN', 'CHUTE', 'CIDER', 'CIGAR', 'CINCH', 'CIRCA', 'CIVIC', 'CIVIL', 'CLACK', 'CLAIM', 'CLAMP', 'CLANG', 'CLANK', 'CLASH', 'CLASP', 'CLASS', 'CLEAN', 'CLEAR', 'CLEAT', 'CLEFT', 'CLERK', 'CLICK', 'CLIFF', 'CLIMB', 'CLING', 'CLINK', 'CLOAK', 'CLOCK', 'CLONE', 'CLOSE', 'CLOTH', 'CLOUD', 'CLOUT', 'CLOVE', 'CLOWN', 'CLUCK', 'CLUED', 'CLUMP', 'CLUNG', 'COACH', 'COAST', 'COBRA', 'COCOA', 'COLON', 'COLOR', 'COMET', 'COMFY', 'COMIC', 'COMMA', 'CONCH', 'CONDO', 'CONIC', 'COPSE', 'CORAL', 'CORER', 'CORNY', 'COUCH', 'COUGH', 'COULD', 'COUNT', 'COUPE', 'COURT', 'COVEN', 'COVER', 'COVET', 'COVEY', 'COWER', 'COYLY', 'CRACK', 'CRAFT', 'CRAMP', 'CRANE', 'CRANK', 'CRASH', 'CRASS', 'CRATE', 'CRAVE', 'CRAWL', 'CRAZE', 'CRAZY', 'CREAK', 'CREAM', 'CREDO', 'CREED', 'CREEK', 'CREEP', 'CREME', 'CREPE', 'CREPT', 'CRESS', 'CREST', 'CRICK', 'CRIED', 'CRIER', 'CRIME', 'CRIMP', 'CRISP', 'CROAK', 'CROCK', 'CRONE', 'CRONY', 'CROOK', 'CROSS', 'CROUP', 'CROWD', 'CROWN', 'CRUDE', 'CRUEL', 'CRUMB', 'CRUMP', 'CRUSH', 'CRUST', 'CRYPT', 'CUBIC', 'CUMIN', 'CURIO', 'CURLY', 'CURRY', 'CURSE', 'CURVE', 'CURVY', 'CUTIE', 'CYBER', 'CYCLE', 'CYNIC', 'DADDY', 'DAILY', 'DAIRY', 'DAISY', 'DALLY', 'DANCE', 'DANDY', 'DATUM', 'DAUNT', 'DEALT', 'DEATH', 'DEBAR', 'DEBIT', 'DEBUG', 'DEBUT', 'DECAL', 'DECAY', 'DECOR', 'DECOY', 'DECRY', 'DEFER', 'DEIGN', 'DEITY', 'DELAY', 'DELTA', 'DELVE', 'DEMON', 'DEMUR', 'DENIM', 'DENSE', 'DEPOT', 'DEPTH', 'DERBY', 'DETER', 'DETOX', 'DEUCE', 'DEVIL', 'DIARY', 'DICEY', 'DIGIT', 'DILLY', 'DIMLY', 'DINER', 'DINGO', 'DINGY', 'DIODE', 'DIRGE', 'DIRTY', 'DISCO', 'DITCH', 'DITTO', 'DITTY', 'DIVER', 'DIZZY', 'DODGE', 'DODGY', 'DOGMA', 'DOING', 'DOLLY', 'DONOR', 'DONUT', 'DOPEY', 'DOUBT', 'DOUGH', 'DOWDY', 'DOWEL', 'DOWNY', 'DOWRY', 'DOZEN', 'DRAFT', 'DRAIN', 'DRAKE', 'DRAMA', 'DRANK', 'DRAPE', 'DRAWL', 'DRAWN', 'DREAD', 'DREAM', 'DRESS', 'DRIED', 'DRIER', 'DRIFT', 'DRILL', 'DRINK', 'DRIVE', 'DROIT', 'DROLL', 'DRONE', 'DROOL', 'DROOP', 'DROSS', 'DROVE', 'DROWN', 'DRUID', 'DRUNK', 'DRYER', 'DRYLY', 'DUCHY', 'DULLY', 'DUMMY', 'DUMPY', 'DUNCE', 'DUSKY', 'DUSTY', 'DUTCH', 'DUVET', 'DWARF', 'DWELL', 'DWELT', 'DYING', 'EAGER', 'EAGLE', 'EARLY', 'EARTH', 'EASEL', 'EATEN', 'EATER', 'EBONY', 'ECLAT', 'EDICT', 'EDIFY', 'EERIE', 'EGRET', 'EIGHT', 'EJECT', 'EKING', 'ELATE', 'ELBOW', 'ELDER', 'ELECT', 'ELEGY', 'ELFIN', 'ELIDE', 'ELITE', 'ELOPE', 'ELUDE', 'EMAIL', 'EMBED', 'EMBER', 'EMCEE', 'EMPTY', 'ENACT', 'ENDOW', 'ENEMA', 'ENEMY', 'ENJOY', 'ENNUI', 'ENSUE', 'ENTER', 'ENTRY', 'ENVOY', 'EPOCH', 'EPOXY', 'EQUAL', 'EQUIP', 'ERASE', 'ERECT', 'ERODE', 'ERROR', 'ERUPT', 'ESSAY', 'ESTER', 'ETHER', 'ETHIC', 'ETHOS', 'ETUDE', 'EVADE', 'EVENT', 'EVERY', 'EVICT', 'EVOKE', 'EXACT', 'EXALT', 'EXCEL', 'EXERT', 'EXILE', 'EXIST', 'EXPEL', 'EXTOL', 'EXTRA', 'EXULT', 'EYING', 'FABLE', 'FACET', 'FAINT', 'FAIRY', 'FAITH', 'FALSE', 'FANCY', 'FANNY', 'FARCE', 'FATAL', 'FATTY', 'FAULT', 'FAUNA', 'FAVOR', 'FEAST', 'FECAL', 'FEIGN', 'FELLA', 'FELON', 'FEMME', 'FEMUR', 'FENCE', 'FERAL', 'FERRY', 'FETAL', 'FETCH', 'FETID', 'FETUS', 'FEVER', 'FEWER', 'FIBER', 'FIBRE', 'FICUS', 'FIELD', 'FIEND', 'FIERY', 'FIFTH', 'FIFTY', 'FIGHT', 'FILER', 'FILET', 'FILLY', 'FILMY', 'FILTH', 'FINAL', 'FINCH', 'FINER', 'FIRST', 'FISHY', 'FIXER', 'FIZZY', 'FJORD', 'FLACK', 'FLAIL', 'FLAIR', 'FLAKE', 'FLAKY', 'FLAME', 'FLANK', 'FLARE', 'FLASH', 'FLASK', 'FLECK', 'FLEET', 'FLESH', 'FLICK', 'FLIER', 'FLING', 'FLINT', 'FLIRT', 'FLOAT', 'FLOCK', 'FLOOD', 'FLOOR', 'FLORA', 'FLOSS', 'FLOUR', 'FLOUT', 'FLOWN', 'FLUFF', 'FLUID', 'FLUKE', 'FLUME', 'FLUNG', 'FLUNK', 'FLUSH', 'FLUTE', 'FLYER', 'FOAMY', 'FOCAL', 'FOCUS', 'FOGGY', 'FOIST', 'FOLIO', 'FOLLY', 'FORAY', 'FORCE', 'FORGE', 'FORGO', 'FORTE', 'FORTH', 'FORTY', 'FORUM', 'FOUND', 'FOYER', 'FRAIL', 'FRAME', 'FRANK', 'FRAUD', 'FREAK', 'FREED', 'FREER', 'FRESH', 'FRIAR', 'FRIED', 'FRILL', 'FRISK', 'FRITZ', 'FROCK', 'FROND', 'FRONT', 'FROST', 'FROTH', 'FROWN', 'FROZE', 'FRUIT', 'FUDGE', 'FUGUE', 'FULLY', 'FUNGI', 'FUNKY', 'FUNNY', 'FUROR', 'FURRY', 'FUSSY', 'FUZZY', 'GAFFE', 'GAILY', 'GAMER', 'GAMMA', 'GAMUT', 'GASSY', 'GAUDY', 'GAUGE', 'GAUNT', 'GAUZE', 'GAVEL', 'GAWKY', 'GAYER', 'GAYLY', 'GAZER', 'GECKO', 'GEEKY', 'GEESE', 'GENIE', 'GENRE', 'GHOST', 'GHOUL', 'GIANT', 'GIDDY', 'GIPSY', 'GIRLY', 'GIRTH', 'GIVEN', 'GIVER', 'GLADE', 'GLAND', 'GLARE', 'GLASS', 'GLAZE', 'GLEAM', 'GLEAN', 'GLIDE', 'GLINT', 'GLOAT', 'GLOBE', 'GLOOM', 'GLORY', 'GLOSS', 'GLOVE', 'GLYPH', 'GNASH', 'GNOME', 'GODLY', 'GOING', 'GOLEM', 'GOLLY', 'GONAD', 'GONER', 'GOODY', 'GOOEY', 'GOOFY', 'GOOSE', 'GORGE', 'GOUGE', 'GOURD', 'GRACE', 'GRADE', 'GRAFT', 'GRAIL', 'GRAIN', 'GRAND', 'GRANT', 'GRAPE', 'GRAPH', 'GRASP', 'GRASS', 'GRATE', 'GRAVE', 'GRAVY', 'GRAZE', 'GREAT', 'GREED', 'GREEN', 'GREET', 'GRIEF', 'GRILL', 'GRIME', 'GRIMY', 'GRIND', 'GRIPE', 'GROAN', 'GROIN', 'GROOM', 'GROPE', 'GROSS', 'GROUP', 'GROUT', 'GROVE', 'GROWL', 'GROWN', 'GRUEL', 'GRUFF', 'GRUNT', 'GUARD', 'GUAVA', 'GUESS', 'GUEST', 'GUIDE', 'GUILD', 'GUILE', 'GUILT', 'GUISE', 'GULCH', 'GULLY', 'GUMBO', 'GUMMY', 'GUPPY', 'GUSTO', 'GUSTY', 'GYPSY', 'HABIT', 'HAIRY', 'HALVE', 'HANDY', 'HAPPY', 'HARDY', 'HAREM', 'HARPY', 'HARRY', 'HARSH', 'HASTE', 'HASTY', 'HATCH', 'HATER', 'HAUNT', 'HAUTE', 'HAVEN', 'HAVOC', 'HAZEL', 'HEADY', 'HEARD', 'HEART', 'HEATH', 'HEAVE', 'HEAVY', 'HEDGE', 'HEFTY', 'HEIST', 'HELIX', 'HELLO', 'HENCE', 'HERON', 'HILLY', 'HINGE', 'HIPPO', 'HIPPY', 'HITCH', 'HOARD', 'HOBBY', 'HOIST', 'HOLLY', 'HOMER', 'HONEY', 'HONOR', 'HORDE', 'HORNY', 'HORSE', 'HOTEL', 'HOTLY', 'HOUND', 'HOUSE', 'HOVEL', 'HOVER', 'HOWDY', 'HUMAN', 'HUMID', 'HUMOR', 'HUMPH', 'HUMUS', 'HUNCH', 'HUNKY', 'HURRY', 'HUSKY', 'HUSSY', 'HUTCH', 'HYDRO', 'HYENA', 'HYMEN', 'HYPER', 'ICILY', 'ICING', 'IDEAL', 'IDIOM', 'IDIOT', 'IDLER', 'IDYLL', 'IGLOO', 'ILIAC', 'IMAGE', 'IMBUE', 'IMPEL', 'IMPLY', 'INANE', 'INBOX', 'INCUR', 'INDEX', 'INEPT', 'INERT', 'INFER', 'INGOT', 'INLAY', 'INLET', 'INNER', 'INPUT', 'INTER', 'INTRO', 'IONIC', 'IRATE', 'IRONY', 'ISLET', 'ISSUE', 'ITCHY', 'IVORY', 'JAUNT', 'JAZZY', 'JELLY', 'JERKY', 'JETTY', 'JEWEL', 'JIFFY', 'JOINT', 'JOIST', 'JOKER', 'JOLLY', 'JOUST', 'JUDGE', 'JUICE', 'JUICY', 'JUMBO', 'JUMPY', 'JUNTA', 'JUNTO', 'JUROR', 'KAPPA', 'KARMA', 'KAYAK', 'KEBAB', 'KHAKI', 'KINKY', 'KIOSK', 'KITTY', 'KNACK', 'KNAVE', 'KNEAD', 'KNEED', 'KNEEL', 'KNELT', 'KNIFE', 'KNOCK', 'KNOLL', 'KNOWN', 'KOALA', 'KRILL', 'LABEL', 'LABOR', 'LADEN', 'LADLE', 'LAGER', 'LANCE', 'LANKY', 'LAPEL', 'LAPSE', 'LARGE', 'LARVA', 'LASSO', 'LATCH', 'LATER', 'LATHE', 'LATTE', 'LAUGH', 'LAYER', 'LEACH', 'LEAFY', 'LEAKY', 'LEANT', 'LEAPT', 'LEARN', 'LEASE', 'LEASH', 'LEAST', 'LEAVE', 'LEDGE', 'LEECH', 'LEERY', 'LEFTY', 'LEGAL', 'LEGGY', 'LEMON', 'LEMUR', 'LEPER', 'LEVEL', 'LEVER', 'LIBEL', 'LIEGE', 'LIGHT', 'LIKEN', 'LILAC', 'LIMBO', 'LIMIT', 'LINEN', 'LINER', 'LINGO', 'LIPID', 'LITHE', 'LIVER', 'LIVID', 'LLAMA', 'LOAMY', 'LOATH', 'LOBBY', 'LOCAL', 'LOCUS', 'LODGE', 'LOFTY', 'LOGIC', 'LOGIN', 'LOOPY', 'LOOSE', 'LORRY', 'LOSER', 'LOUSE', 'LOUSY', 'LOVER', 'LOWER', 'LOWLY', 'LOYAL', 'LUCID', 'LUCKY', 'LUMEN', 'LUMPY', 'LUNAR', 'LUNCH', 'LUNGE', 'LUPUS', 'LURCH', 'LURID', 'LUSTY', 'LYING', 'LYMPH', 'LYNCH', 'LYRIC', 'MACAW', 'MACHO', 'MACRO', 'MADAM', 'MADLY', 'MAFIA', 'MAGIC', 'MAGMA', 'MAIZE', 'MAJOR', 'MAKER', 'MAMBO', 'MAMMA', 'MAMMY', 'MANGA', 'MANGE', 'MANGO', 'MANGY', 'MANIA', 'MANIC', 'MANLY', 'MANOR', 'MAPLE', 'MARCH', 'MARRY', 'MARSH', 'MASON', 'MASSE', 'MATCH', 'MATEY', 'MAUVE', 'MAXIM', 'MAYBE', 'MAYOR', 'MEALY', 'MEANT', 'MEATY', 'MECCA', 'MEDAL', 'MEDIA', 'MEDIC', 'MELEE', 'MELON', 'MERCY', 'MERGE', 'MERIT', 'MERRY', 'METAL', 'METER', 'METRO', 'MICRO', 'MIDGE', 'MIDST', 'MIGHT', 'MILKY', 'MIMIC', 'MINCE', 'MINER', 'MINIM', 'MINOR', 'MINTY', 'MINUS', 'MIRTH', 'MISER', 'MISSY', 'MOCHA', 'MODAL', 'MODEL', 'MODEM', 'MOGUL', 'MOIST', 'MOLAR', 'MOLDY', 'MONEY', 'MONTH', 'MOODY', 'MOOSE', 'MORAL', 'MORON', 'MORPH', 'MOSSY', 'MOTEL', 'MOTIF', 'MOTOR', 'MOTTO', 'MOULT', 'MOUND', 'MOUNT', 'MOURN', 'MOUSE', 'MOUTH', 'MOVER', 'MOVIE', 'MOWER', 'MUCKY', 'MUCUS', 'MUDDY', 'MULCH', 'MUMMY', 'MUNCH', 'MURAL', 'MURKY', 'MUSHY', 'MUSIC', 'MUSKY', 'MUSTY', 'MYRRH', 'NADIR', 'NAIVE', 'NANNY', 'NASAL', 'NASTY', 'NATAL', 'NAVAL', 'NAVEL', 'NEEDY', 'NEIGH', 'NERDY', 'NERVE', 'NEVER', 'NEWER', 'NEWLY', 'NICER', 'NICHE', 'NIECE', 'NIGHT', 'NINJA', 'NINNY', 'NINTH', 'NOBLE', 'NOBLY', 'NOISE', 'NOISY', 'NOMAD', 'NOOSE', 'NORTH', 'NOSEY', 'NOTCH', 'NOVEL', 'NUDGE', 'NURSE', 'NUTTY', 'NYLON', 'NYMPH', 'OAKEN', 'OBESE', 'OCCUR', 'OCEAN', 'OCTAL', 'OCTET', 'ODDER', 'ODDLY', 'OFFAL', 'OFFER', 'OFTEN', 'OLDEN', 'OLDER', 'OLIVE', 'OMBRE', 'OMEGA', 'ONION', 'ONSET', 'OPERA', 'OPINE', 'OPIUM', 'OPTIC', 'ORBIT', 'ORDER', 'ORGAN', 'OTHER', 'OTTER', 'OUGHT', 'OUNCE', 'OUTDO', 'OUTER', 'OUTGO', 'OVARY', 'OVATE', 'OVERT', 'OVINE', 'OVOID', 'OWING', 'OWNER', 'OXIDE', 'OZONE', 'PADDY', 'PAGAN', 'PAINT', 'PALER', 'PALSY', 'PANEL', 'PANIC', 'PANSY', 'PAPAL', 'PAPER', 'PARER', 'PARKA', 'PARRY', 'PARSE', 'PARTY', 'PASTA', 'PASTE', 'PASTY', 'PATCH', 'PATIO', 'PATSY', 'PATTY', 'PAUSE', 'PAYEE', 'PAYER', 'PEACE', 'PEACH', 'PEARL', 'PECAN', 'PEDAL', 'PENAL', 'PENCE', 'PENNE', 'PENNY', 'PERCH', 'PERIL', 'PERKY', 'PESKY', 'PESTO', 'PETAL', 'PETTY', 'PHASE', 'PHONE', 'PHONY', 'PHOTO', 'PIANO', 'PICKY', 'PIECE', 'PIETY', 'PIGGY', 'PILOT', 'PINCH', 'PINEY', 'PINKY', 'PINTO', 'PIPER', 'PIQUE', 'PITCH', 'PITHY', 'PIVOT', 'PIXEL', 'PIXIE', 'PIZZA', 'PLACE', 'PLAID', 'PLAIN', 'PLAIT', 'PLANE', 'PLANK', 'PLANT', 'PLATE', 'PLAZA', 'PLEAD', 'PLEAT', 'PLIED', 'PLIER', 'PLUCK', 'PLUMB', 'PLUME', 'PLUMP', 'PLUNK', 'PLUSH', 'POESY', 'POINT', 'POISE', 'POKER', 'POLAR', 'POLKA', 'POLYP', 'POOCH', 'POPPY', 'PORCH', 'POSER', 'POSIT', 'POSSE', 'POUCH', 'POUND', 'POUTY', 'POWER', 'PRANK', 'PRAWN', 'PREEN', 'PRESS', 'PRICE', 'PRICK', 'PRIDE', 'PRIED', 'PRIME', 'PRIMO', 'PRINT', 'PRIOR', 'PRISM', 'PRIVY', 'PRIZE', 'PROBE', 'PRONE', 'PRONG', 'PROOF', 'PROSE', 'PROUD', 'PROVE', 'PROWL', 'PROXY', 'PRUDE', 'PRUNE', 'PSALM', 'PUBIC', 'PUDGY', 'PUFFY', 'PULPY', 'PULSE', 'PUNCH', 'PUPAL', 'PUPIL', 'PUPPY', 'PUREE', 'PURER', 'PURGE', 'PURSE', 'PUSHY', 'PUTTY', 'PYGMY', 'QUACK', 'QUAIL', 'QUAKE', 'QUALM', 'QUARK', 'QUART', 'QUASH', 'QUASI', 'QUEEN', 'QUEER', 'QUELL', 'QUERY', 'QUEST', 'QUEUE', 'QUICK', 'QUIET', 'QUILL', 'QUILT', 'QUIRK', 'QUITE', 'QUOTA', 'QUOTE', 'QUOTH', 'RABBI', 'RABID', 'RACER', 'RADAR', 'RADII', 'RADIO', 'RAINY', 'RAISE', 'RAJAH', 'RALLY', 'RALPH', 'RAMEN', 'RANCH', 'RANDY', 'RANGE', 'RAPID', 'RARER', 'RASPY', 'RATIO', 'RATTY', 'RAVEN', 'RAYON', 'RAZOR', 'REACH', 'REACT', 'READY', 'REALM', 'REARM', 'REBAR', 'REBEL', 'REBUS', 'REBUT', 'RECAP', 'RECUR', 'RECUT', 'REEDY', 'REFER', 'REFIT', 'REGAL', 'REHAB', 'REIGN', 'RELAX', 'RELAY', 'RELIC', 'REMIT', 'RENAL', 'RENEW', 'REPAY', 'REPEL', 'REPLY', 'RERUN', 'RESET', 'RESIN', 'RETCH', 'RETRO', 'RETRY', 'REUSE', 'REVEL', 'REVUE', 'RHINO', 'RHYME', 'RIDER', 'RIDGE', 'RIFLE', 'RIGHT', 'RIGID', 'RIGOR', 'RINSE', 'RIPEN', 'RIPER', 'RISEN', 'RISER', 'RISKY', 'RIVAL', 'RIVER', 'RIVET', 'ROACH', 'ROAST', 'ROBIN', 'ROBOT', 'ROCKY', 'RODEO', 'ROGER', 'ROGUE', 'ROOMY', 'ROOST', 'ROTOR', 'ROUGE', 'ROUGH', 'ROUND', 'ROUSE', 'ROUTE', 'ROVER', 'ROWDY', 'ROWER', 'ROYAL', 'RUDDY', 'RUDER', 'RUGBY', 'RULER', 'RUMBA', 'RUMOR', 'RUPEE', 'RURAL', 'RUSTY', 'SADLY', 'SAFER', 'SAINT', 'SALAD', 'SALLY', 'SALON', 'SALSA', 'SALTY', 'SALVE', 'SALVO', 'SANDY', 'SANER', 'SAPPY', 'SASSY', 'SATIN', 'SATYR', 'SAUCE', 'SAUCY', 'SAUNA', 'SAUTE', 'SAVOR', 'SAVOY', 'SAVVY', 'SCALD', 'SCALE', 'SCALP', 'SCALY', 'SCAMP', 'SCANT', 'SCARE', 'SCARF', 'SCARY', 'SCENE', 'SCENT', 'SCION', 'SCOFF', 'SCOLD', 'SCONE', 'SCOOP', 'SCOPE', 'SCORE', 'SCORN', 'SCOUR', 'SCOUT', 'SCOWL', 'SCRAM', 'SCRAP', 'SCREE', 'SCREW', 'SCRUB', 'SCRUM', 'SCUBA', 'SEDAN', 'SEEDY', 'SEGUE', 'SEIZE', 'SEMEN', 'SENSE', 'SEPIA', 'SERIF', 'SERUM', 'SERVE', 'SETUP', 'SEVEN', 'SEVER', 'SEWER', 'SHACK', 'SHADE', 'SHADY', 'SHAFT', 'SHAKE', 'SHAKY', 'SHALE', 'SHALL', 'SHALT', 'SHAME', 'SHANK', 'SHAPE', 'SHARD', 'SHARE', 'SHARK', 'SHARP', 'SHAVE', 'SHAWL', 'SHEAR', 'SHEEN', 'SHEEP', 'SHEER', 'SHEET', 'SHEIK', 'SHELF', 'SHELL', 'SHIED', 'SHIFT', 'SHINE', 'SHINY', 'SHIRE', 'SHIRK', 'SHIRT', 'SHOAL', 'SHOCK', 'SHONE', 'SHOOK', 'SHOOT', 'SHORE', 'SHORN', 'SHORT', 'SHOUT', 'SHOVE', 'SHOWN', 'SHOWY', 'SHREW', 'SHRUB', 'SHRUG', 'SHUCK', 'SHUNT', 'SHUSH', 'SHYLY', 'SIEGE', 'SIEVE', 'SIGHT', 'SIGMA', 'SILKY', 'SILLY', 'SINCE', 'SINEW', 'SINGE', 'SIREN', 'SISSY', 'SIXTH', 'SIXTY', 'SKATE', 'SKIER', 'SKIFF', 'SKILL', 'SKIMP', 'SKIRT', 'SKULK', 'SKULL', 'SKUNK', 'SLACK', 'SLAIN', 'SLANG', 'SLANT', 'SLASH', 'SLATE', 'SLAVE', 'SLEEK', 'SLEEP', 'SLEET', 'SLEPT', 'SLICE', 'SLICK', 'SLIDE', 'SLIME', 'SLIMY', 'SLING', 'SLINK', 'SLOOP', 'SLOPE', 'SLOSH', 'SLOTH', 'SLUMP', 'SLUNG', 'SLUNK', 'SLURP', 'SLUSH', 'SLYLY', 'SMACK', 'SMALL', 'SMART', 'SMASH', 'SMEAR', 'SMELL', 'SMELT', 'SMILE', 'SMIRK', 'SMITE', 'SMITH', 'SMOCK', 'SMOKE', 'SMOKY', 'SMOTE', 'SNACK', 'SNAIL', 'SNAKE', 'SNAKY', 'SNARE', 'SNARL', 'SNEAK', 'SNEER', 'SNIDE', 'SNIFF', 'SNIPE', 'SNOOP', 'SNORE', 'SNORT', 'SNOUT', 'SNOWY', 'SNUCK', 'SNUFF', 'SOAPY', 'SOBER', 'SOGGY', 'SOLAR', 'SOLID', 'SOLVE', 'SONAR', 'SONIC', 'SOOTH', 'SOOTY', 'SORRY', 'SOUND', 'SOUTH', 'SOWER', 'SPACE', 'SPADE', 'SPANK', 'SPARE', 'SPARK', 'SPASM', 'SPAWN', 'SPEAK', 'SPEAR', 'SPECK', 'SPEED', 'SPELL', 'SPELT', 'SPEND', 'SPENT', 'SPERM', 'SPICE', 'SPICY', 'SPIED', 'SPIEL', 'SPIKE', 'SPIKY', 'SPILL', 'SPILT', 'SPINE', 'SPINY', 'SPIRE', 'SPITE', 'SPLAT', 'SPLIT', 'SPOIL', 'SPOKE', 'SPOOF', 'SPOOK', 'SPOOL', 'SPOON', 'SPORE', 'SPORT', 'SPOUT', 'SPRAY', 'SPREE', 'SPRIG', 'SPUNK', 'SPURN', 'SPURT', 'SQUAD', 'SQUAT', 'SQUIB', 'STACK', 'STAFF', 'STAGE', 'STAID', 'STAIN', 'STAIR', 'STAKE', 'STALE', 'STALK', 'STALL', 'STAMP', 'STAND', 'STANK', 'STARE', 'STARK', 'START', 'STASH', 'STATE', 'STAVE', 'STEAD', 'STEAK', 'STEAL', 'STEAM', 'STEED', 'STEEL', 'STEEP', 'STEER', 'STEIN', 'STERN', 'STICK', 'STIFF', 'STILL', 'STILT', 'STING', 'STINK', 'STINT', 'STOCK', 'STOIC', 'STOKE', 'STOLE', 'STOMP', 'STONE', 'STONY', 'STOOD', 'STOOL', 'STOOP', 'STORE', 'STORK', 'STORM', 'STORY', 'STOUT', 'STOVE', 'STRAP', 'STRAW', 'STRAY', 'STRIP', 'STRUT', 'STUCK', 'STUDY', 'STUFF', 'STUMP', 'STUNG', 'STUNK', 'STUNT', 'STYLE', 'SUAVE', 'SUGAR', 'SUING', 'SUITE', 'SULKY', 'SULLY', 'SUMAC', 'SUNNY', 'SUPER', 'SURER', 'SURGE', 'SURLY', 'SUSHI', 'SWAMI', 'SWAMP', 'SWARM', 'SWASH', 'SWATH', 'SWEAR', 'SWEAT', 'SWEEP', 'SWEET', 'SWELL', 'SWEPT', 'SWIFT', 'SWILL', 'SWINE', 'SWING', 'SWIRL', 'SWISH', 'SWOON', 'SWOOP', 'SWORD', 'SWORE', 'SWORN', 'SWUNG', 'SYNOD', 'SYRUP', 'TABBY', 'TABLE', 'TABOO', 'TACIT', 'TACKY', 'TAFFY', 'TAINT', 'TAKEN', 'TAKER', 'TALLY', 'TALON', 'TAMER', 'TANGO', 'TANGY', 'TAPER', 'TAPIR', 'TARDY', 'TAROT', 'TASTE', 'TASTY', 'TATTY', 'TAUNT', 'TAWNY', 'TEACH', 'TEARY', 'TEASE', 'TEDDY', 'TEETH', 'TEMPO', 'TENET', 'TENOR', 'TENSE', 'TENTH', 'TEPEE', 'TEPID', 'TERRA', 'TERSE', 'TESTY', 'THANK', 'THEFT', 'THEIR', 'THEME', 'THERE', 'THESE', 'THETA', 'THICK', 'THIEF', 'THIGH', 'THING', 'THINK', 'THIRD', 'THONG', 'THORN', 'THOSE', 'THREE', 'THREW', 'THROB', 'THROW', 'THRUM', 'THUMB', 'THUMP', 'THYME', 'TIARA', 'TIBIA', 'TIDAL', 'TIGER', 'TIGHT', 'TILDE', 'TIMER', 'TIMID', 'TIPSY', 'TITAN', 'TITHE', 'TITLE', 'TOAST', 'TODAY', 'TODDY', 'TOKEN', 'TONAL', 'TONGA', 'TONIC', 'TOOTH', 'TOPAZ', 'TOPIC', 'TORCH', 'TORSO', 'TORUS', 'TOTAL', 'TOTEM', 'TOUCH', 'TOUGH', 'TOWEL', 'TOWER', 'TOXIC', 'TOXIN', 'TRACE', 'TRACK', 'TRACT', 'TRADE', 'TRAIL', 'TRAIN', 'TRAIT', 'TRAMP', 'TRASH', 'TRAWL', 'TREAD', 'TREAT', 'TREND', 'TRIAD', 'TRIAL', 'TRIBE', 'TRICE', 'TRICK', 'TRIED', 'TRIPE', 'TRITE', 'TROLL', 'TROOP', 'TROPE', 'TROUT', 'TROVE', 'TRUCE', 'TRUCK', 'TRUER', 'TRULY', 'TRUMP', 'TRUNK', 'TRUSS', 'TRUST', 'TRUTH', 'TRYST', 'TUBAL', 'TUBER', 'TULIP', 'TULLE', 'TUMOR', 'TUNIC', 'TURBO', 'TUTOR', 'TWANG', 'TWEAK', 'TWEED', 'TWEET', 'TWICE', 'TWINE', 'TWIRL', 'TWIST', 'TWIXT', 'TYING', 'UDDER', 'ULCER', 'ULTRA', 'UMBRA', 'UNCLE', 'UNCUT', 'UNDER', 'UNDID', 'UNDUE', 'UNFED', 'UNFIT', 'UNIFY', 'UNION', 'UNITE', 'UNITY', 'UNLIT', 'UNMET', 'UNSET', 'UNTIE', 'UNTIL', 'UNWED', 'UNZIP', 'UPPER', 'UPSET', 'URBAN', 'URINE', 'USAGE', 'USHER', 'USING', 'USUAL', 'USURP', 'UTILE', 'UTTER', 'VAGUE', 'VALET', 'VALID', 'VALOR', 'VALUE', 'VALVE', 'VAPID', 'VAPOR', 'VAULT', 'VAUNT', 'VEGAN', 'VENOM', 'VENUE', 'VERGE', 'VERSE', 'VERSO', 'VERVE', 'VICAR', 'VIDEO', 'VIGIL', 'VIGOR', 'VILLA', 'VINYL', 'VIOLA', 'VIPER', 'VIRAL', 'VIRUS', 'VISIT', 'VISOR', 'VISTA', 'VITAL', 'VIVID', 'VIXEN', 'VOCAL', 'VODKA', 'VOGUE', 'VOICE', 'VOILA', 'VOMIT', 'VOTER', 'VOUCH', 'VOWEL', 'VYING', 'WACKY', 'WAFER', 'WAGER', 'WAGON', 'WAIST', 'WAIVE', 'WALTZ', 'WARTY', 'WASTE', 'WATCH', 'WATER', 'WAVER', 'WAXEN', 'WEARY', 'WEAVE', 'WEDGE', 'WEEDY', 'WEIGH', 'WEIRD', 'WELCH', 'WELSH', 'WENCH', 'WHACK', 'WHALE', 'WHARF', 'WHEAT', 'WHEEL', 'WHELP', 'WHERE', 'WHICH', 'WHIFF', 'WHILE', 'WHINE', 'WHINY', 'WHIRL', 'WHISK', 'WHITE', 'WHOLE', 'WHOOP', 'WHOSE', 'WIDEN', 'WIDER', 'WIDOW', 'WIDTH', 'WIELD', 'WIGHT', 'WILLY', 'WIMPY', 'WINCE', 'WINCH', 'WINDY', 'WISER', 'WISPY', 'WITCH', 'WITTY', 'WOKEN', 'WOMAN', 'WOMEN', 'WOODY', 'WOOER', 'WOOLY', 'WOOZY', 'WORDY', 'WORLD', 'WORRY', 'WORSE', 'WORST', 'WORTH', 'WOULD', 'WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST', 'WRING', 'WRIST', 'WRITE', 'WRONG', 'WROTE', 'WRUNG', 'WRYLY', 'YACHT', 'YEARN', 'YEAST', 'YIELD', 'YOUNG', 'YOUTH', 'ZEBRA', 'ZESTY', 'ZONAL']
    return możliwe_hasła



def menu():
    while True:
        okno.fill(tło)
        tekst_w_kracie("WORDLE", czcionka_duże, czarny, pygame.Rect(0, 50, szerokość_okna, 100))

        standardowy_przycisk = pygame.Rect(155, 250, 200, 50)
        czasowy_przycisk = pygame.Rect(155, 350, 200, 50)

        pygame.draw.rect(okno, czerwony, standardowy_przycisk)
        pygame.draw.rect(okno, czerwony, czasowy_przycisk)

        tekst_w_kracie("Standardowa Gra", czcionka_małe, czarny, standardowy_przycisk)
        tekst_w_kracie("Gra Na Czas", czcionka_małe, czarny, czasowy_przycisk)

        pygame.display.flip()

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                if standardowy_przycisk.collidepoint(zdarzenie.pos):
                    main(False)
                elif czasowy_przycisk.collidepoint(zdarzenie.pos):
                    main(True)

def main(czasowy):
    możliwe_hasła = lista_haseł()
    hasło = random.choice(możliwe_hasła)

    próby = [[''] * kolumny for _ in range(rzędy)]
    kolory = [[biały] * kolumny for _ in range(rzędy)]
    próba_teraz = ''
    rząd = 0
    start_czas = time.time() if czasowy else None
    limit_czasu = 120 if czasowy else None

    while True:
        if czasowy:
            pozostały_czas = max(0, limit_czasu - int(time.time() - start_czas))
            if pozostały_czas <= 0:
                pokaz_wiadomość("Czas się skończył. Hasło to: " + hasło)
                return
        else:
            pozostały_czas = None

        krata()
        rysuj_tekst(próby, kolory, próba_teraz, rząd, pozostały_czas)

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif zdarzenie.type == pygame.KEYDOWN:
                if zdarzenie.key == pygame.K_BACKSPACE:
                    próba_teraz = próba_teraz[:-1]
                elif zdarzenie.key == pygame.K_RETURN:
                    if len(próba_teraz) == kolumny:
                        zielone, zolte, szare = sprawdzanie(hasło, próba_teraz)
                        for i, litera in enumerate(próba_teraz):
                            if (litera, i) in zielone:
                                kolory[rząd][i] = zielony
                            elif (litera, i) in zolte:
                                kolory[rząd][i] = żółty
                            elif (litera, i) in szare:
                                kolory[rząd][i] = szary
                        próby[rząd] = list(próba_teraz)
                        rząd += 1
                        if próba_teraz == hasło:
                            pokaz_wiadomość("Gratulacje, hasło odgadnięte poprawnie")
                            return
                        próba_teraz = ''
                        if rząd >= rzędy:
                            pokaz_wiadomość("Przegrałeś. Hasło to: " + hasło)
                            return
                elif zdarzenie.unicode.isalpha() and len(próba_teraz) < kolumny:
                    próba_teraz += zdarzenie.unicode.upper()

        pygame.display.flip()

def pokaz_wiadomość(wiadomość):
    while True:
        okno.fill(tło)
        tekst_w_kracie(wiadomość, czcionka_małe, czarny, pygame.Rect(0, wysokość_okna // 2 - 50, szerokość_okna, 100))

        przycisk_menu = pygame.Rect(szerokość_okna // 2 - 100, wysokość_okna // 2 + 100, 200, 50)
        pygame.draw.rect(okno, zielony, przycisk_menu)
        tekst_w_kracie("Wróć do menu", czcionka_małe, czarny, przycisk_menu)

        pygame.display.flip()

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                if przycisk_menu.collidepoint(zdarzenie.pos):
                    return

if __name__ == "__main__":
    menu()
