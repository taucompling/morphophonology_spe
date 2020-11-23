simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 0,
        "MERGE_EMISSIONS": 0,
        "ADVANCE_EMISSION": 1,
        "CLONE_STATE": 0,
        "CLONE_EMISSION": 1,
        "SPLIT_EMISSION": 0,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "MERGE_STATES": 1,
        "SPLIT_STATES": 0,
        "ADD_TRANSITION": 1,
        "REMOVE_TRANSITION": 1,
        "ADD_SEGMENT_TO_EMISSION": 1,
        "REMOVE_SEGMENT_FROM_EMISSION": 1,
        "CHANGE_SEGMENT_IN_EMISSION": 1,
        "ADD_EMISSION_TO_STATE": 1,
        "REMOVE_EMISSION_FROM_STATE": 1,
        "ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

        "DATA_ENCODING_LENGTH_MULTIPLIER": 10,
        "HMM_ENCODING_LENGTH_MULTIPLIER": 25,
        "RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

        "ADD_RULE": 1,
        "REMOVE_RULE": 1,
        "DEMOTE_RULE": 1,
        "CHANGE_RULE": 1,

        "MUTATE_TARGET": 1,
        "MUTATE_CHANGE": 1,
        "MUTATE_LEFT_CONTEXT": 1,
        "MUTATE_RIGHT_CONTEXT": 1,
        "MUTATE_OBLIGATORY": 1,
        "SWITCH_TARGET_CHANGE": 0,

        "ADD_FEATURE_BUNDLE": 1,
        "REMOVE_FEATURE_BUNDLE": 1,
        "CHANGE_EXISTING_FEATURE_BUNDLE": 1,

        "ADD_FEATURE": 1,
        "REMOVE_FEATURE": 1,
        "CHANGE_FEATURE_VALUE": 1,
        "CHANGE_KLEENE_VALUE": 0,

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

        "MAX_NUM_OF_INNER_STATES": 4,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 4,
        "MIN_NUMBER_OF_RULES": 0,

        "MORPHEME_BOUNDARY_FLAG": True,
        "LENGTHENING_FLAG": False,
        "UNDERSPECIFICATION_FLAG": False,
        "WORD_BOUNDARY_FLAG": False,
        "RESTRICTIONS_ON_ALPHABET": False,

        # Genetic algorithm params

        "CROSSOVER_RATE": 0.2,
        "MUTATION_RATE": 0.8,
        "CROSSOVER_COOLING_RATE": 1.0,
        "MUTATION_COOLING_RATE": 1.0,
        "VAR_AND": False,
        "TOTAL_GENERATIONS": 30000,
        "REPRODUCTION_LAMBDA": 0.8,
        "SELECTION_METHOD": "rank",  # ["tournament", "rank"]
        "RANK_SELECTION_PRESSURE": 1.7,
        "TOURNAMENT_SIZE": 2,

        # Island model params
        "ISLAND_POPULATION": 200,
        "MIGRATION_INTERVAL": 30,
        "MIGRATION_RATIO": 0.2,
        "ISLAND_ELITE_RATIO": 0.1,
        "MIGRATION_SCHEME": "round_robin",  # ["fixed", "round_robin"]

        # HMM
        "HMM_CROSSOVER_METHOD": "emissions",  # ['emissions', 'matrix', 'subgraph', 'connected_component']"
        "LIMIT_CROSSOVER_RESULT_HMM_NUM_OF_STATES": True,
        "HMM_MAX_CROSSOVERS": 1,
        "RANDOM_HMM_MAX_EMISSION_LENGTH": 3,
        "RANDOM_HMM_MAX_EMISSIONS_PER_STATE": 15,
        "RANDOM_HMM_METHOD": 'simple',  # ['simple', 'matrix']
        "HMM_RANDOM_EMISSIONS_BY_DATA": True,  # HMM random emissions will be substrings of data words
        "DEFAULT_HMM_BY_RANDOM_PROBAB": 0.0,
        "EXPLICIT_HMM_BY_RANDOM_PROBAB": 0.0,
        "TRANSITION_MATRIX_TRANSITION_PROBABILITY": 0.1,

        # Rule set
        "RULE_SET_CROSSOVER_METHOD": "switch_pairs",  # ['unilateral', 'switch_pairs', 'pivot'],

        # Transducers
        "MINIMIZE_TRANSDUCER": False,
        "TRANSDUCER_STATES_LIMIT": 1000,
        "DFAS_STATES_LIMIT": 1000
    }

log_file_template = "{}_french_two_rules_small_{}.txt"

segment_table_file_name = "french_two_rules.txt"

data = ['arb', 'arbabil', 'arbbas', 'arbfad', 'arbfiab', 'arbfiabl', 'arbpuri', 'arbr', 'arbrabil', 'arbrbas', 'arbrebas', 'arbrefad', 'arbrefiab', 'arbrefiabl', 'arbrepuri', 'arbresal', 'arbresup', 'arbresupl', 'arbretimid', 'arbrfad', 'arbrfiab', 'arbrfiabl', 'arbrpuri', 'arbrsal', 'arbrsup', 'arbrsupl', 'arbrtimid', 'arbsal', 'arbsup', 'arbsupl', 'arbtimid', 'fil', 'filabil', 'filbas', 'filfad', 'filfiab', 'filfiabl', 'filpuri', 'filsal', 'filsup', 'filsupl', 'filt', 'filtabil', 'filtbas', 'filtfad', 'filtfiab', 'filtfiabl', 'filtimid', 'filtpuri', 'filtr', 'filtrabil', 'filtrbas', 'filtrebas', 'filtrefad', 'filtrefiab', 'filtrefiabl', 'filtrepuri', 'filtresal', 'filtresup', 'filtresupl', 'filtretimid', 'filtrfad', 'filtrfiab', 'filtrfiabl', 'filtrpuri', 'filtrsal', 'filtrsup', 'filtrsupl', 'filtrtimid', 'filtsal', 'filtsup', 'filtsupl', 'filttimid', 'klop', 'klopabil', 'klopbas', 'klopfad', 'klopfiab', 'klopfiabl', 'kloppuri', 'klopsal', 'klopsup', 'klopsupl', 'kloptimid', 'krab', 'krababil', 'krabbas', 'krabfad', 'krabfiab', 'krabfiabl', 'krabpuri', 'krabsal', 'krabsup', 'krabsupl', 'krabtimid', 'kuverk', 'kuverkabil', 'kuverkbas', 'kuverkfad', 'kuverkfiab', 'kuverkfiabl', 'kuverkl', 'kuverklabil', 'kuverklbas', 'kuverklebas', 'kuverklefad', 'kuverklefiab', 'kuverklefiabl', 'kuverklepuri', 'kuverklesal', 'kuverklesup', 'kuverklesupl', 'kuverkletimid', 'kuverklfad', 'kuverklfiab', 'kuverklfiabl', 'kuverklpuri', 'kuverklsal', 'kuverklsup', 'kuverklsupl', 'kuverkltimid', 'kuverkpuri', 'kuverksal', 'kuverksup', 'kuverksupl', 'kuverktimid', 'liv', 'livabil', 'livbas', 'livfad', 'livfiab', 'livfiabl', 'livpuri', 'livr', 'livrabil', 'livrbas', 'livrebas', 'livrefad', 'livrefiab', 'livrefiabl', 'livrepuri', 'livresal', 'livresup', 'livresupl', 'livretimid', 'livrfad', 'livrfiab', 'livrfiabl', 'livrpuri', 'livrsal', 'livrsup', 'livrsupl', 'livrtimid', 'livsal', 'livsup', 'livsupl', 'livtimid', 'parl', 'parlabil', 'parlbas', 'parlebas', 'parlefad', 'parlefiab', 'parlefiabl', 'parlepuri', 'parlesal', 'parlesup', 'parlesupl', 'parletimid', 'parlfad', 'parlfiab', 'parlfiabl', 'parlpuri', 'parlsal', 'parlsup', 'parlsupl', 'parltimid', 'purp', 'purpabil', 'purpbas', 'purpfad', 'purpfiab', 'purpfiabl', 'purppuri', 'purpr', 'purprabil', 'purprbas', 'purprebas', 'purprefad', 'purprefiab', 'purprefiabl', 'purprepuri', 'purpresal', 'purpresup', 'purpresupl', 'purpretimid', 'purprfad', 'purprfiab', 'purprfiabl', 'purprpuri', 'purprsal', 'purprsup', 'purprsupl', 'purprtimid', 'purpsal', 'purpsup', 'purpsupl', 'purptimid', 'rob', 'robabil', 'robbas', 'robfad', 'robfiab', 'robfiabl', 'robpuri', 'robsal', 'robsup', 'robsupl', 'robtimid', 'sak', 'sakabil', 'sakbas', 'sakfad', 'sakfiab', 'sakfiabl', 'sakpuri', 'saksal', 'saksup', 'saksupl', 'saktimid', 'strof', 'strofabil', 'strofbas', 'stroffad', 'stroffiab', 'stroffiabl', 'strofpuri', 'strofsal', 'strofsup', 'strofsupl', 'stroftimid', 'tab', 'tababil', 'tabbas', 'tabfad', 'tabfiab', 'tabfiabl', 'tabl', 'tablabil', 'tablbas', 'tablebas', 'tablefad', 'tablefiab', 'tablefiabl', 'tablepuri', 'tablesal', 'tablesup', 'tablesupl', 'tabletimid', 'tablfad', 'tablfiab', 'tablfiabl', 'tablpuri', 'tablsal', 'tablsup', 'tablsupl', 'tabltimid', 'tabpuri', 'tabsal', 'tabsup', 'tabsupl', 'tabtimid']


from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q3'],
                     ['tabl', 'arbr', 'livr', 'kuverkl', 'fil', 'parl', 'purpr', 'filtr', 'krab', 'klop', 'grat',
                      'sak', 'strof', 'esclav', 'rob']),
              'q3': (['qf'], ['sal', 'fiabl', 'supl', 'puri', 'abil', 'timid', 'bas', 'fad', EPSILON])}

schwa_epenthesis = [[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"MB": True}, {"cons": "+"}], False]
l_deletion = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False]

rule_set = [schwa_epenthesis, l_deletion]

# initial_hmm = {'q0': ['q1'],
#                'q1': (['qf'], data[:])
#                }

target_tuple = (target_hmm, rule_set)