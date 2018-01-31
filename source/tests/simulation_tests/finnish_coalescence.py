from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class FinnishCoalescence(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("finnish_coalescence_segment_table.txt")
        self.data = [u'tattiatten', u'tattiataenta', u'tattiadappe', u'tattiamimbe', u'tattiaanmid', u'tattiaanei', u'tattiaaettiema', u'tattiaapentem', u'tattiaademna', u'tattiaatta', u'tattiapiet', u'tattia', u'teimiatten', u'teimiataenta', u'teimiadappe', u'teimiamimbe', u'teimiaanmid', u'teimiaanei', u'teimiaaettiema', u'teimiaapentem', u'teimiaademna', u'teimiaatta', u'teimiapiet', u'teimia', u'dametten', u'dametaenta', u'damedappe', u'damemimbe', u'dameenmid', u'dameenei', u'dameeettiema', u'dameepentem', u'dameedemna', u'dameetta', u'dameanmid', u'dameanei', u'dameaettiema', u'dameapentem', u'dameademna', u'dameatta', u'damepiet', u'dame', u'maettetten', u'maettetaenta', u'maettedappe', u'maettemimbe', u'maetteenmid', u'maetteenei', u'maetteeettiema', u'maetteepentem', u'maetteedemna', u'maetteetta', u'maetteanmid', u'maetteanei', u'maetteaettiema', u'maetteapentem', u'maetteademna', u'maetteatta', u'maettepiet', u'maette', u'niemdaetetten', u'niemdaetetaenta', u'niemdaetedappe', u'niemdaetemimbe', u'niemdaeteenmid', u'niemdaeteenei', u'niemdaeteeettiema', u'niemdaeteepentem', u'niemdaeteedemna', u'niemdaeteetta', u'niemdaeteanmid', u'niemdaeteanei', u'niemdaeteaettiema', u'niemdaeteapentem', u'niemdaeteademna', u'niemdaeteatta', u'niemdaetepiet', u'niemdaete', u'naettabtten', u'naettabtaenta', u'naettabdappe', u'naettabmimbe', u'naettabanmid', u'naettabanei', u'naettabaettiema', u'naettabapentem', u'naettabademna', u'naettabatta', u'naettabpiet', u'naettab', u'ainiatten', u'ainiataenta', u'ainiadappe', u'ainiamimbe', u'ainiaanmid', u'ainiaanei', u'ainiaaettiema', u'ainiaapentem', u'ainiaademna', u'ainiaatta', u'ainiapiet', u'ainia', u'ippemtten', u'ippemtaenta', u'ippemdappe', u'ippemmimbe', u'ippemanmid', u'ippemanei', u'ippemaettiema', u'ippemapentem', u'ippemademna', u'ippematta', u'ippempiet', u'ippem', u'pamintatten', u'pamintataenta', u'pamintadappe', u'pamintamimbe', u'pamintaanmid', u'pamintaanei', u'pamintaaettiema', u'pamintaapentem', u'pamintaademna', u'pamintaatta', u'pamintapiet', u'paminta', u'pimetten', u'pimetaenta', u'pimedappe', u'pimemimbe', u'pimeenmid', u'pimeenei', u'pimeeettiema', u'pimeepentem', u'pimeedemna', u'pimeetta', u'pimeanmid', u'pimeanei', u'pimeaettiema', u'pimeapentem', u'pimeademna', u'pimeatta', u'pimepiet', u'pime', u'bindattten', u'bindattaenta', u'bindatdappe', u'bindatmimbe', u'bindatanmid', u'bindatanei', u'bindataettiema', u'bindatapentem', u'bindatademna', u'bindatatta', u'bindatpiet', u'bindat', u'bentetten', u'bentetaenta', u'bentedappe', u'bentemimbe', u'benteenmid', u'benteenei', u'benteeettiema', u'benteepentem', u'benteedemna', u'benteetta', u'benteanmid', u'benteanei', u'benteaettiema', u'benteapentem', u'benteademna', u'benteatta', u'bentepiet', u'bente']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 1


    def test_(self):
        self.target_energy = None

        hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['maette','pime','dame','bente','niemdaete','teimia','paminta','tattia','ainia', 'bindat', 'ippem', 'naettab']),
              'q2': (['qf'], ['atta','anei', 'aettiema', "apentem", 'ademna', 'anmid', 'taenta', 'tten', "mimbe", "piet", "dappe"])}

        coalescence_rule = [[{"low": "+"}], [{"low": "-"}], [{"cons": "-", "high": "-", "low":"-"}], [], False]
        target = SimulationCase("target", hmm, [coalescence_rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], list("pbtdmnaei")),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)

        hmm = {'q0': ['q1'],
              'q1': (['q2','q3','qf'], ['maette','pime','dame','bente','niemdaete','teimia','paminta','tattia','ainia', 'bindat', 'ippem', 'naettab']),
              'q2': (['q3'], ['a','e']),
              'q3': (['qf'], ['atta','tta','nei', 'ettiema', "pentem", 'demna', 'nmid', 'taenta', 'tten', "mimbe", "piet", "dappe"])}


        with_ea = SimulationCase("with_ea", hmm, [coalescence_rule])
        self.get_energy(with_ea)
