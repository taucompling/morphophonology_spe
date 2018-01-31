from tests.my_test_case import MyTestCase
from configuration import PrefixDict


class TestUtils(MyTestCase):
    def setUp(self):
        pass

    def test_prefix_dict(self):
        words = ['ban', 'banka', 'bankestr', 'banket', 'bankik', 'banks', 'blan', 'blanka', 'blankestr', 'blanket',
                 'blankik', 'blanks', 'blau', 'blaua', 'blauestr', 'blauet', 'blauik', 'blaus', 'brut', 'bruta',
                 'brutestr', 'brutet', 'brutik', 'bruts', 'dolen', 'dolenta', 'dolentestr', 'dolentet', 'dolentik',
                 'dolents', 'elefan', 'elefanta', 'elefantestr', 'elefantet', 'elefantik', 'elefants', 'fu', 'fuma',
                 'fumestr', 'fumet', 'fumik', 'fums', 'gra', 'grana', 'granestr', 'granet', 'granik', 'grans', 'gris',
                 'grisa', 'grisestr', 'griset', 'grisik', 'griss', 'kaima', 'kaimana', 'kaimanestr', 'kaimanet',
                 'kaimanik', 'kaimans', 'kalen', 'kalenta', 'kalentestr', 'kalentet', 'kalentik', 'kalents', 'kam',
                 'kampa', 'kampestr', 'kampet', 'kampik', 'kamps', 'kap', 'kapa', 'kapestr', 'kapet', 'kapik', 'kaps',
                 'kasa', 'kasaa', 'kasaestr', 'kasaet', 'kasaik', 'kasas', 'katala', 'katalana', 'katalanestr',
                 'katalanet', 'katalanik', 'katalans', 'kuzi', 'kuzina', 'kuzinestr', 'kuzinet', 'kuzinik', 'kuzins',
                 'len', 'lenta', 'lentestr', 'lentet', 'lentik', 'lents', 'leo', 'leona', 'leonestr', 'leonet',
                 'leonik', 'leons', 'mal', 'mala', 'malestr', 'malet', 'malik', 'mals', 'metal', 'metala', 'metalestr',
                 'metalet', 'metalik', 'metals', 'nebot', 'nebota', 'nebotestr', 'nebotet', 'nebotik', 'nebots',
                 'negre', 'negrea', 'negreestr', 'negreet', 'negreik', 'negres', 'pikan', 'pikanta', 'pikantestr',
                 'pikantet', 'pikantik', 'pikants', 'pla', 'plana', 'planestr', 'planet', 'planik', 'plans', 'plasa',
                 'plasaa', 'plasaestr', 'plasaet', 'plasaik', 'plasas', 'pri', 'prima', 'primestr', 'primet', 'primik',
                 'prims', 'profun', 'profunda', 'profundestr', 'profundet', 'profundik', 'profunds', 'sile', 'silena',
                 'silenestr', 'silenet', 'silenik', 'silens', 'telefo', 'telefona', 'telefonestr', 'telefonet',
                 'telefonik', 'telefons', 'tin', 'tinka', 'tinkestr', 'tinket', 'tinkik', 'tinks']
        prefix_dict = PrefixDict(words)
        print(prefix_dict.words_by_prefix)
        print(prefix_dict.prefixes_by_word)
