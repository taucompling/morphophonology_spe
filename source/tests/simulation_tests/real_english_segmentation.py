from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration
from segment_table import SegmentTable

configurations = Configuration()

class RealEnglishSegmentation(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("real_english_segmentation_segment_table.txt")
        self.data = ['abberation', 'abberations', 'abbreviate', 'abbreviated', 'abbreviates', 'abolitionist', 'abolitionists', 'abortion', 'abortions', 'absence', 'absences', 'abstractionist', 'abstractionists', 'abutment', 'abutments', 'accent', 'accented', 'accenting', 'accents', 'acclaim', 'acclaimed', 'acclaims', 'accolade', 'accolades', 'accommodate', 'accommodated', 'accommodates', 'accommodation', 'accommodations', 'accomodation', 'accomodations', 'achieve', 'achieved', 'achieves', 'achieving', 'add', 'added', 'adding', 'adds', 'administer', 'administered', 'administering', 'administers', 'advertise', 'advertised', 'advertiser', 'advertises', 'advertising', 'afford', 'afforded', 'affording', 'affords', 'aggravate', 'aggravated', 'aggravates', 'alert', 'alerted', 'alerting', 'alerts', 'amount', 'amounted', 'amounting', 'amounts', 'announce', 'announced', 'announcer', 'announces', 'announcing', 'appeal', 'appealed', 'appealing', 'appeals', 'applaud', 'applauded', 'applauding', 'apprentice', 'apprenticed', 'apprentices', 'arcade', 'arcaded', 'arcades', 'arrest', 'arrested', 'arresting', 'assault', 'assaulted', 'assaulting', 'assaults', 'assume', 'assumed', 'assumes', 'assuming', 'astound', 'astounded', 'astounding', 'attack', 'attacked', 'attacker', 'attacking', 'attacks', 'attempt', 'attempted', 'attempting', 'attempts', 'back', 'backed', 'backer', 'backing', 'backs', 'bake', 'baked', 'baker', 'bakes', 'baking', 'balance', 'balanced', 'balances', 'barbecue', 'barbecued', 'barbecues', 'bath', 'bathed', 'bather', 'bathing', 'baths', 'beckon', 'beckoned', 'beckons', 'benefit', 'benefited', 'benefits', 'blast', 'blasted', 'blasting', 'blend', 'blended', 'blends', 'bless', 'blessed', 'blessing', 'blister', 'blistered', 'blisters', 'bloom', 'bloomed', 'blooming', 'blow', 'blower', 'blowing', 'blows', 'boast', 'boasted', 'boasting', 'bogey', 'bogeyed', 'bogeys', 'boil', 'boiled', 'boiler', 'boiling', 'boils', 'bolster', 'bolstered', 'bolstering', 'bomb', 'bomber', 'bombing', 'bombs', 'borrow', 'borrowed', 'borrower', 'borrowing', 'borrows', 'bother', 'bothered', 'bothers', 'brace', 'braced', 'braces', 'bracing', 'breakfast', 'breakfasted', 'breakfasts', 'broadcast', 'broadcaster', 'broadcasting', 'broadcasts', 'broaden', 'broadened', 'broadening', 'bruise', 'bruised', 'bruises', 'buffet', 'buffeted', 'buffets', 'burden', 'burdened', 'burdens', 'catalogue', 'catalogued', 'catalogues', 'cater', 'catered', 'catering', 'challenge', 'challenged', 'challenger', 'challenges', 'challenging', 'change', 'changed', 'changes', 'changing', 'charge', 'charged', 'charges', 'charging', 'charm', 'charmed', 'charmer', 'charming', 'charms', 'comprise', 'comprised', 'comprises', 'comprising', 'concede', 'conceded', 'concedes', 'conceding', 'conclude', 'concluded', 'concludes', 'concluding', 'condition', 'conditioned', 'conditioner', 'conditioning', 'conditions', 'consume', 'consumed', 'consumer', 'consumes', 'consuming', 'costume', 'costumed', 'costumes', 'deal', 'dealer', 'dealing', 'deals', 'decide', 'decided', 'decides', 'deciding', 'demand', 'demanded', 'demander', 'demanding', 'demands', 'describe', 'described', 'describes', 'describing', 'down', 'downed', 'downer', 'downing', 'downs', 'draw', 'drawer', 'drawing', 'draws', 'drink', 'drinker', 'drinking', 'drinks', 'dwell', 'dweller', 'dwelling', 'dwells', 'enforce', 'enforced', 'enforcer', 'enforces', 'enforcing', 'farm', 'farmer', 'farming', 'farms', 'feed', 'feeder', 'feeding', 'feeds', 'feel', 'feeler', 'feeling', 'feels', 'flow', 'flowed', 'flower', 'flowing', 'flows', 'gaze', 'gazed', 'gazer', 'gazes', 'gazing', 'glaze', 'glazed', 'glazer', 'glazes', 'glazing', 'invade', 'invaded', 'invader', 'invades', 'invading', 'live', 'lived', 'liver', 'lives', 'living', 'pace', 'paced', 'pacer', 'paces', 'pacing']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 10
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 1


    def test_(self):
        self.target_energy = None
        hmm = {'q0': ['q1'],
            'q1': (['q2','qf'], ['abberation', 'abbreviate', 'abolitionist', 'abortion', 'absence', 'abstractionist', 'abutment', 'accent', 'acclaim', 'accolade', 'accommodate', 'accommodation', 'accomodation', 'achiev', 'add', 'administer', 'advertis', 'afford', 'aggravate', 'alert', 'amount', 'announc', 'appeal', 'applaud', 'apprentice', 'arcade', 'arrest', 'assault', 'assum', 'astound', 'attack', 'attempt', 'back', 'bak', 'balance', 'barbecue', 'bath', 'beckon', 'benefit', 'blast', 'blend', 'bless', 'blister', 'bloom', 'blow', 'boast', 'bogey', 'boil', 'bolster', 'bomb', 'borrow', 'bother', 'brac', 'breakfast', 'broadcast', 'broaden', 'bruise', 'buffet', 'burden', 'catalogue', 'cater', 'challeng', 'chang', 'charg', 'charm', 'compris', 'conced', 'conclud', 'condition', 'consum', 'costume', 'deal', 'decid', 'demand', 'describ', 'down', 'draw', 'drink', 'dwell', 'enforc', 'farm', 'feed', 'feel', 'flow', 'gaz', 'glaz', 'invad', 'liv', 'pac']),
            'q2': (['qf'], ['ing', 'e', 'd', 'ed', 's', 'es', 'er'])
              }

        target = SimulationCase("target", hmm, [])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], SegmentTable().get_segments_symbols()),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)



        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], self.data[:]),
              }

        rote_learning = SimulationCase("rote_learning", hmm, [])
        self.get_energy(rote_learning)

