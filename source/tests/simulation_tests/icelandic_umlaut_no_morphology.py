from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

# [7/25/15, 10:17:20 PM] iddo berger: meur
# [7/25/15, 10:18:21 PM] iddo berger: ruem
# [7/25/15, 10:19:45 PM] iddo berger: gaag
# [7/25/15, 10:20:14 PM] iddo berger: deag
# [7/25/15, 10:20:51 PM] iddo berger: uat


more_words = ['meur', 'ruem', 'gaag', 'deag', 'uat']

inputs = more_words +['katr', 'derr', 'edr', 'dekruk', 'marut', 'amr', 'damuk', 'gamuk', 'tedruk', 'merrer', 'medr', 'kudr', 'ramutk', 'remr', 'redrem', 'ugr', 'matram', 'gegr', 'memegr', 'rerr', 'magram', 'kakekr', 'tederr', 'kamr', 'ruratr', 'tatum', 'akr', 'mamakr', 'ekr', 'redr', 'makred', 'kutegr', 'darut', 'gamud', 'mudr', 'karrad', 'err', 'ragug', 'taruk', 'gatukd', 'katudt', 'tamug', 'mamudt', 'madum', 'rakutm', 'kamut', 'kamud', 'kakudg', 'mamuk', 'tagurk', 'tarugr', 'dadugk', 'tarumm', 'ramud', 'kaduk']

outputs = more_words + ['katur', 'derur', 'edur', 'dekuruk', 'maYrut', 'amur', 'daYmuk', 'gaYmuk', 'teduruk', 'merurer', 'medur', 'kudur', 'raYmutk', 'remur', 'redurem', 'ugur', 'maturam', 'gegur', 'memegur', 'rerur', 'maguram', 'kakekur', 'tederur', 'kamur', 'ruratur', 'taYtum', 'akur', 'mamakur', 'ekur', 'redur', 'makured', 'kutegur', 'daYrut', 'gaYmud', 'mudur', 'karurad', 'erur', 'raYgug', 'taYruk', 'gaYtukd', 'kaYtudt', 'taYmug', 'maYmudt', 'maYdum', 'raYkutm', 'kaYmut', 'kaYmud', 'kaYkudg', 'maYmuk', 'taYgurk', 'taYrugur', 'daYdugk', 'taYrumm', 'raYmud', 'kaYduk']

class IcelandicUmlautNoMorphology(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("icelandic_umlaut_no_morphology_segment_table.txt")
        self.data = outputs
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 100
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 25


    def test_(self):
        self.target_energy = None

        hmm = {'q0': ['q1'],
              'q1': (['qf'], inputs)
              }

        umlaut_rule = [[], [{"round": "+", "back": "-"}],  [{"low": "+"}],  [{"cons": "+"}, {"round": "+"}], True]
        u_epenthesis_rule = [[], [{"low": "-", "back": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True]

        target = SimulationCase("target", hmm, [umlaut_rule, u_epenthesis_rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], outputs),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)



        words = ['aur', 'daYugk', 'daYuk', 'daYut', 'deur', 'deuuk', 'eur', 'gaYud', 'gaYuk', 'gaYukd', 'geur', 'kaYduk', u'kaYud', 'kaYudg', 'kaYudt', u'kaYut', 'kaeur', 'kauad', 'kaur', 'kueur', 'kuur', 'maYudt', 'maYuk', u'maYum', 'maYut', u'maaur', 'mauam', u'maued', 'medur', 'meeur', u'meuer', 'muur', 'raYud', 'raYug', 'raYutk', 'raYutm', 'reuem', 'reur', 'ruaur', u'taYrumm', 'taYug', u'taYuk', 'taYum', u'taYurk', 'taYuur', 'teeur', u'teuuk', 'uur']
        hmm = {'q0': ['q1'],
            'q1': (['qf'], words),
              }

        rule = [[], [{'cons': '+', 'low': '-'}], [{'cons': '-'}], [{'velar': '-', 'voice': '+', 'cons': '-', 'rhotic': '-'}], True]

        from_simulation1 = SimulationCase("from_simulation1", hmm, [rule])
        self.get_energy(from_simulation1)
