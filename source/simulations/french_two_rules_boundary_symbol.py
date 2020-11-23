raise Exception("This version of the corpus doesnt lead to a different encoding length for the alternative rule order. Need to debug. Do not use")

simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 1,
        "MERGE_EMISSIONS": 0,
        "ADVANCE_EMISSION": 1,
        "MOVE_EMISSION": 1,
        "CLONE_STATE": 0,
        "CLONE_EMISSION": 1,
        "SPLIT_EMISSION": 1,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "MERGE_STATES": 0,
        "SPLIT_STATES": 0,
        "ADD_TRANSITION": 1,
        "REMOVE_TRANSITION": 1,
        "ADD_SEGMENT_TO_EMISSION": 1,
        "REMOVE_SEGMENT_FROM_EMISSION": 1,
        "CHANGE_SEGMENT_IN_EMISSION": 1,
        "ADD_EMISSION_TO_STATE": 1,
        "REMOVE_EMISSION_FROM_STATE": 1,
        "ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

        "DATA_ENCODING_LENGTH_MULTIPLIER": 50,
        "HMM_ENCODING_LENGTH_MULTIPLIER": 20,
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

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 3,

        "MAX_NUM_OF_INNER_STATES": 3,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 3,
        "MIN_NUMBER_OF_RULES": 0,

        "MORPHEME_BOUNDARY_FLAG": False,
        "LENGTHENING_FLAG": False,
        "UNDERSPECIFICATION_FLAG": False,
        "WORD_BOUNDARY_FLAG": False,
        "RESTRICTIONS_ON_ALPHABET": False,

        # Genetic algorithm params

        "CROSSOVER_RATE": 0.1,
        "MUTATION_RATE": 0.9,
        "CROSSOVER_COOLING_RATE": 1.0,
        "MUTATION_COOLING_RATE": 1.0,
        "VAR_AND": False,
        "TOTAL_GENERATIONS": 100000,
        "REPRODUCTION_LAMBDA": 0.8,
        "SELECTION_METHOD": "rank",  # ["tournament", "rank"]
        "RANK_SELECTION_PRESSURE": 1.7,
        "TOURNAMENT_SIZE": 2,

        # Island model params
        "ISLAND_POPULATION": 250,
        "MIGRATION_INTERVAL": 30,
        "MIGRATION_RATIO": 0.2,
        "ISLAND_ELITE_RATIO": 0.1,
        "MIGRATION_SCHEME": "round_robin",  # ["fixed", "round_robin"]

        # HMM
        "HMM_CROSSOVER_METHOD": "emissions",  # ['emissions', 'matrix', 'subgraph', 'connected_component']"
        "LIMIT_CROSSOVER_RESULT_HMM_NUM_OF_STATES": True,
        "HMM_MAX_CROSSOVERS": 1,
        "RANDOM_HMM_MAX_EMISSION_LENGTH": 10,
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

log_file_template = "{}_french_two_rules_{}.txt"

segment_table_file_name = "french_two_rules_boundary_symbol.txt"

data = ['amurX', 'amurXabilX', 'amurXbyvablX', 'amurXfadX', 'amurXivrX', 'amurXkifX', 'amurXmalX', 'amurXpuriX', 'amurXtimidX', 'arbrX', 'arbrXabilX', 'arbrXbyvablX', 'arbrXfadX', 'arbrXivrX', 'arbrXkifX', 'arbrXmalX', 'arbrXpuriX', 'arbrXtimidX', 'batirX', 'batirXabilX', 'batirXbyvablX', 'batirXfadX', 'batirXivrX', 'batirXkifX', 'batirXmalX', 'batirXpuriX', 'batirXtimidX', 'burkX', 'burkXabilX', 'burkXbyvablX', 'burkXfadX', 'burkXivrX', 'burkXkifX', 'burkXmalX', 'burkXpuriX', 'burkXtimidX', 'bylX', 'bylXabilX', 'bylXbyvablX', 'bylXfadX', 'bylXivrX', 'bylXkifX', 'bylXmalX', 'bylXpuriX', 'bylXtimidX', 'dartrX', 'dartrXabilX', 'dartrXbyvablX', 'dartrXfadX', 'dartrXivrX', 'dartrXkifX', 'dartrXmalX', 'dartrXpuriX', 'dartrXtimidX', 'filmX', 'filmXabilX', 'filmXbyvablX', 'filmXfadX', 'filmXivrX', 'filmXkifX', 'filmXmalX', 'filmXpuriX', 'filmXtimidX', 'filtrX', 'filtrXabilX', 'filtrXbyvablX', 'filtrXfadX', 'filtrXivrX', 'filtrXkifX', 'filtrXmalX', 'filtrXpuriX', 'filtrXtimidX', 'furyrX', 'furyrXabilX', 'furyrXbyvablX', 'furyrXfadX', 'furyrXivrX', 'furyrXkifX', 'furyrXmalX', 'furyrXpuriX', 'furyrXtimidX', 'kaptX', 'kaptXabilX', 'kaptXbyvablX', 'kaptXfadX', 'kaptXivrX', 'kaptXkifX', 'kaptXmalX', 'kaptXpuriX', 'kaptXtimidX', 'karafX', 'karafXabilX', 'karafXbyvablX', 'karafXfadX', 'karafXivrX', 'karafXkifX', 'karafXmalX', 'karafXpuriX', 'karafXtimidX', 'kladX', 'kladXabilX', 'kladXbyvablX', 'kladXfadX', 'kladXivrX', 'kladXkifX', 'kladXmalX', 'kladXpuriX', 'kladXtimidX', 'klopX', 'klopXabilX', 'klopXbyvablX', 'klopXfadX', 'klopXivrX', 'klopXkifX', 'klopXmalX', 'klopXpuriX', 'klopXtimidX', 'krabX', 'krabXabilX', 'krabXbyvablX', 'krabXfadX', 'krabXivrX', 'krabXkifX', 'krabXmalX', 'krabXpuriX', 'krabXtimidX', 'kuplX', 'kuplXabilX', 'kuplXbyvablX', 'kuplXfadX', 'kuplXivrX', 'kuplXkifX', 'kuplXmalX', 'kuplXpuriX', 'kuplXtimidX', 'kurbX', 'kurbXabilX', 'kurbXbyvablX', 'kurbXfadX', 'kurbXivrX', 'kurbXkifX', 'kurbXmalX', 'kurbXpuriX', 'kurbXtimidX', 'kuverklX', 'kuverklXabilX', 'kuverklXbyvablX', 'kuverklXfadX', 'kuverklXivrX', 'kuverklXkifX', 'kuverklXmalX', 'kuverklXpuriX', 'kuverklXtimidX', 'kyltX', 'kyltXabilX', 'kyltXbyvablX', 'kyltXfadX', 'kyltXivrX', 'kyltXkifX', 'kyltXmalX', 'kyltXpuriX', 'kyltXtimidX', 'mordrX', 'mordrXabilX', 'mordrXbyvablX', 'mordrXfadX', 'mordrXivrX', 'mordrXkifX', 'mordrXmalX', 'mordrXpuriX', 'mordrXtimidX', 'odorX', 'odorXabilX', 'odorXbyvablX', 'odorXfadX', 'odorXivrX', 'odorXkifX', 'odorXmalX', 'odorXpuriX', 'odorXtimidX', 'parlX', 'parlXabilX', 'parlXbyvablX', 'parlXfadX', 'parlXivrX', 'parlXkifX', 'parlXmalX', 'parlXpuriX', 'parlXtimidX', 'provokX', 'provokXabilX', 'provokXbyvablX', 'provokXfadX', 'provokXivrX', 'provokXkifX', 'provokXmalX', 'provokXpuriX', 'provokXtimidX', 'prutX', 'prutXabilX', 'prutXbyvablX', 'prutXfadX', 'prutXivrX', 'prutXkifX', 'prutXmalX', 'prutXpuriX', 'prutXtimidX', 'purprX', 'purprXabilX', 'purprXbyvablX', 'purprXfadX', 'purprXivrX', 'purprXkifX', 'purprXmalX', 'purprXpuriX', 'purprXtimidX', 'romprX', 'romprXabilX', 'romprXbyvablX', 'romprXfadX', 'romprXivrX', 'romprXkifX', 'romprXmalX', 'romprXpuriX', 'romprXtimidX', 'tablX', 'tablXabilX', 'tablXbyvablX', 'tablXfadX', 'tablXivrX', 'tablXkifX', 'tablXmalX', 'tablXpuriX', 'tablXtimidX', 'yrlX', 'yrlXabilX', 'yrlXbyvablX', 'yrlXfadX', 'yrlXivrX', 'yrlXkifX', 'yrlXmalX', 'yrlXpuriX', 'yrlXtimidX']


target_hmm = {'q0': ['q1'],
              'q1': (['q2'],
                     ['klop', 'kylt', 'provok', 'prut', 'klad', 'krab', 'mordr', 'tabl', 'arbr', 'parl',
                      'yrl', 'burk', 'kurb', 'kapt', 'kupl', 'film', 'odor', 'amur', 'karaf', 'furyr', 'byl',
                      'batir', 'purpr', 'kuverkl', 'filtr', 'rompr', 'dartr']),
              'q2': (['q3', 'qf'], ['X']),
              'q3': (['q4'], ['kif', 'timid', 'fad', 'mal', 'byvabl', 'puri', 'abil', 'ivr']),
              'q4': (['qf'], ['X'])}

_initial_hmm = {'q0': ['q1'],
                'q1': (['qf'], data[:])
                }

schwa_epenthesis = [[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"mb": "+"}, {"cons": "+"}], False]
l_deletion = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"mb": "+"}], False]

rule_set = [schwa_epenthesis, l_deletion]

target_tuple = (target_hmm, rule_set)