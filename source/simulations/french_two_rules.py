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

        "DATA_ENCODING_LENGTH_MULTIPLIER": 1,
        "HMM_ENCODING_LENGTH_MULTIPLIER": 1,
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

        "MORPHEME_BOUNDARY_FLAG": True,
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
        "TOTAL_GENERATIONS": 100_000,
        "REPRODUCTION_LAMBDA": 0.8,
        "SELECTION_METHOD": "rank",  # ["tournament", "rank"]
        "RANK_SELECTION_PRESSURE": 1.7,
        "TOURNAMENT_SIZE": 2,

        # Island model params
        "ISLAND_POPULATION": 450,
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
        "RULE_SET_CROSSOVER_METHOD": "unilateral",  # ['unilateral', 'switch_pairs', 'pivot'],

        # Transducers
        "MINIMIZE_TRANSDUCER": False,
        "TRANSDUCER_STATES_LIMIT": 1000,
        "DFAS_STATES_LIMIT": 1000
    }

log_file_template = "{}_french_two_rules_{}.txt"

segment_table_file_name = "french_two_rules.txt"

data = ['amur', 'amurabil', 'amurbyf', 'amurbyfl', 'amurbyvab', 'amurbyvabl', 'amurdub', 'amurdubl', 'amurfad', 'amurformidab', 'amurformidabl', 'amurfut', 'amurfutr', 'amuriv', 'amurivr', 'amurkif', 'amurmal', 'amurprobab', 'amurprobabl', 'amurpuri', 'amurtimid', 'arb', 'arbabil', 'arbbyf', 'arbbyfl', 'arbbyvab', 'arbbyvabl', 'arbdub', 'arbdubl', 'arbfad', 'arbformidab', 'arbformidabl', 'arbfut', 'arbfutr', 'arbiv', 'arbivr', 'arbkif', 'arbmal', 'arbprobab', 'arbprobabl', 'arbpuri', 'arbr', 'arbrabil', 'arbrbyf', 'arbrbyfl', 'arbrbyvab', 'arbrbyvabl', 'arbrdub', 'arbrdubl', 'arbrebyf', 'arbrebyfl', 'arbrebyvab', 'arbrebyvabl', 'arbredub', 'arbredubl', 'arbrefad', 'arbreformidab', 'arbreformidabl', 'arbrefut', 'arbrefutr', 'arbrekif', 'arbremal', 'arbreprobab', 'arbreprobabl', 'arbrepuri', 'arbretimid', 'arbrfad', 'arbrformidab', 'arbrformidabl', 'arbrfut', 'arbrfutr', 'arbriv', 'arbrivr', 'arbrkif', 'arbrmal', 'arbrprobab', 'arbrprobabl', 'arbrpuri', 'arbrtimid', 'arbtimid', 'batir', 'batirabil', 'batirbyf', 'batirbyfl', 'batirbyvab', 'batirbyvabl', 'batirdub', 'batirdubl', 'batirfad', 'batirformidab', 'batirformidabl', 'batirfut', 'batirfutr', 'batiriv', 'batirivr', 'batirkif', 'batirmal', 'batirprobab', 'batirprobabl', 'batirpuri', 'batirtimid', 'bib', 'bibabil', 'bibbyf', 'bibbyfl', 'bibbyvab', 'bibbyvabl', 'bibdub', 'bibdubl', 'bibfad', 'bibformidab', 'bibformidabl', 'bibfut', 'bibfutr', 'bibiv', 'bibivr', 'bibkif', 'bibl', 'biblabil', 'biblbyf', 'biblbyfl', 'biblbyvab', 'biblbyvabl', 'bibldub', 'bibldubl', 'biblebyf', 'biblebyfl', 'biblebyvab', 'biblebyvabl', 'bibledub', 'bibledubl', 'biblefad', 'bibleformidab', 'bibleformidabl', 'biblefut', 'biblefutr', 'biblekif', 'biblemal', 'bibleprobab', 'bibleprobabl', 'biblepuri', 'bibletimid', 'biblfad', 'biblformidab', 'biblformidabl', 'biblfut', 'biblfutr', 'bibliv', 'biblivr', 'biblkif', 'biblmal', 'biblprobab', 'biblprobabl', 'biblpuri', 'bibltimid', 'bibmal', 'bibprobab', 'bibprobabl', 'bibpuri', 'bibtimid', 'byl', 'bylabil', 'bylbyf', 'bylbyfl', 'bylbyvab', 'bylbyvabl', 'byldub', 'byldubl', 'bylfad', 'bylformidab', 'bylformidabl', 'bylfut', 'bylfutr', 'byliv', 'bylivr', 'bylkif', 'bylmal', 'bylprobab', 'bylprobabl', 'bylpuri', 'byltimid', 'dart', 'dartabil', 'dartbyf', 'dartbyfl', 'dartbyvab', 'dartbyvabl', 'dartdub', 'dartdubl', 'dartfad', 'dartformidab', 'dartformidabl', 'dartfut', 'dartfutr', 'dartiv', 'dartivr', 'dartkif', 'dartmal', 'dartprobab', 'dartprobabl', 'dartpuri', 'dartr', 'dartrabil', 'dartrbyf', 'dartrbyfl', 'dartrbyvab', 'dartrbyvabl', 'dartrdub', 'dartrdubl', 'dartrebyf', 'dartrebyfl', 'dartrebyvab', 'dartrebyvabl', 'dartredub', 'dartredubl', 'dartrefad', 'dartreformidab', 'dartreformidabl', 'dartrefut', 'dartrefutr', 'dartrekif', 'dartremal', 'dartreprobab', 'dartreprobabl', 'dartrepuri', 'dartretimid', 'dartrfad', 'dartrformidab', 'dartrformidabl', 'dartrfut', 'dartrfutr', 'dartriv', 'dartrivr', 'dartrkif', 'dartrmal', 'dartrprobab', 'dartrprobabl', 'dartrpuri', 'dartrtimid', 'darttimid', 'film', 'filmabil', 'filmbyf', 'filmbyfl', 'filmbyvab', 'filmbyvabl', 'filmdub', 'filmdubl', 'filmebyf', 'filmebyfl', 'filmebyvab', 'filmebyvabl', 'filmedub', 'filmedubl', 'filmefad', 'filmeformidab', 'filmeformidabl', 'filmefut', 'filmefutr', 'filmekif', 'filmemal', 'filmeprobab', 'filmeprobabl', 'filmepuri', 'filmetimid', 'filmfad', 'filmformidab', 'filmformidabl', 'filmfut', 'filmfutr', 'filmiv', 'filmivr', 'filmkif', 'filmmal', 'filmprobab', 'filmprobabl', 'filmpuri', 'filmtimid', 'filt', 'filtabil', 'filtbyf', 'filtbyfl', 'filtbyvab', 'filtbyvabl', 'filtdub', 'filtdubl', 'filtfad', 'filtformidab', 'filtformidabl', 'filtfut', 'filtfutr', 'filtiv', 'filtivr', 'filtkif', 'filtmal', 'filtprobab', 'filtprobabl', 'filtpuri', 'filtr', 'filtrabil', 'filtrbyf', 'filtrbyfl', 'filtrbyvab', 'filtrbyvabl', 'filtrdub', 'filtrdubl', 'filtrebyf', 'filtrebyfl', 'filtrebyvab', 'filtrebyvabl', 'filtredub', 'filtredubl', 'filtrefad', 'filtreformidab', 'filtreformidabl', 'filtrefut', 'filtrefutr', 'filtrekif', 'filtremal', 'filtreprobab', 'filtreprobabl', 'filtrepuri', 'filtretimid', 'filtrfad', 'filtrformidab', 'filtrformidabl', 'filtrfut', 'filtrfutr', 'filtriv', 'filtrivr', 'filtrkif', 'filtrmal', 'filtrprobab', 'filtrprobabl', 'filtrpuri', 'filtrtimid', 'filttimid', 'furyr', 'furyrabil', 'furyrbyf', 'furyrbyfl', 'furyrbyvab', 'furyrbyvabl', 'furyrdub', 'furyrdubl', 'furyrfad', 'furyrformidab', 'furyrformidabl', 'furyrfut', 'furyrfutr', 'furyriv', 'furyrivr', 'furyrkif', 'furyrmal', 'furyrprobab', 'furyrprobabl', 'furyrpuri', 'furyrtimid', 'kapt', 'kaptabil', 'kaptbyf', 'kaptbyfl', 'kaptbyvab', 'kaptbyvabl', 'kaptdub', 'kaptdubl', 'kaptebyf', 'kaptebyfl', 'kaptebyvab', 'kaptebyvabl', 'kaptedub', 'kaptedubl', 'kaptefad', 'kapteformidab', 'kapteformidabl', 'kaptefut', 'kaptefutr', 'kaptekif', 'kaptemal', 'kapteprobab', 'kapteprobabl', 'kaptepuri', 'kaptetimid', 'kaptfad', 'kaptformidab', 'kaptformidabl', 'kaptfut', 'kaptfutr', 'kaptiv', 'kaptivr', 'kaptkif', 'kaptmal', 'kaptprobab', 'kaptprobabl', 'kaptpuri', 'kapttimid', 'karaf', 'karafabil', 'karafbyf', 'karafbyfl', 'karafbyvab', 'karafbyvabl', 'karafdub', 'karafdubl', 'karaffad', 'karafformidab', 'karafformidabl', 'karaffut', 'karaffutr', 'karafiv', 'karafivr', 'karafkif', 'karafmal', 'karafprobab', 'karafprobabl', 'karafpuri', 'karaftimid', 'klad', 'kladabil', 'kladbyf', 'kladbyfl', 'kladbyvab', 'kladbyvabl', 'kladdub', 'kladdubl', 'kladfad', 'kladformidab', 'kladformidabl', 'kladfut', 'kladfutr', 'kladiv', 'kladivr', 'kladkif', 'kladmal', 'kladprobab', 'kladprobabl', 'kladpuri', 'kladtimid', 'klop', 'klopabil', 'klopbyf', 'klopbyfl', 'klopbyvab', 'klopbyvabl', 'klopdub', 'klopdubl', 'klopfad', 'klopformidab', 'klopformidabl', 'klopfut', 'klopfutr', 'klopiv', 'klopivr', 'klopkif', 'klopmal', 'klopprobab', 'klopprobabl', 'kloppuri', 'kloptimid', 'krab', 'krababil', 'krabbyf', 'krabbyfl', 'krabbyvab', 'krabbyvabl', 'krabdub', 'krabdubl', 'krabfad', 'krabformidab', 'krabformidabl', 'krabfut', 'krabfutr', 'krabiv', 'krabivr', 'krabkif', 'krabmal', 'krabprobab', 'krabprobabl', 'krabpuri', 'krabtimid', 'kup', 'kupabil', 'kupbyf', 'kupbyfl', 'kupbyvab', 'kupbyvabl', 'kupdub', 'kupdubl', 'kupfad', 'kupformidab', 'kupformidabl', 'kupfut', 'kupfutr', 'kupiv', 'kupivr', 'kupkif', 'kupl', 'kuplabil', 'kuplbyf', 'kuplbyfl', 'kuplbyvab', 'kuplbyvabl', 'kupldub', 'kupldubl', 'kuplebyf', 'kuplebyfl', 'kuplebyvab', 'kuplebyvabl', 'kupledub', 'kupledubl', 'kuplefad', 'kupleformidab', 'kupleformidabl', 'kuplefut', 'kuplefutr', 'kuplekif', 'kuplemal', 'kupleprobab', 'kupleprobabl', 'kuplepuri', 'kupletimid', 'kuplfad', 'kuplformidab', 'kuplformidabl', 'kuplfut', 'kuplfutr', 'kupliv', 'kuplivr', 'kuplkif', 'kuplmal', 'kuplprobab', 'kuplprobabl', 'kuplpuri', 'kupltimid', 'kupmal', 'kupprobab', 'kupprobabl', 'kuppuri', 'kuptimid', 'kurb', 'kurbabil', 'kurbbyf', 'kurbbyfl', 'kurbbyvab', 'kurbbyvabl', 'kurbdub', 'kurbdubl', 'kurbebyf', 'kurbebyfl', 'kurbebyvab', 'kurbebyvabl', 'kurbedub', 'kurbedubl', 'kurbefad', 'kurbeformidab', 'kurbeformidabl', 'kurbefut', 'kurbefutr', 'kurbekif', 'kurbemal', 'kurbeprobab', 'kurbeprobabl', 'kurbepuri', 'kurbetimid', 'kurbfad', 'kurbformidab', 'kurbformidabl', 'kurbfut', 'kurbfutr', 'kurbiv', 'kurbivr', 'kurbkif', 'kurbmal', 'kurbprobab', 'kurbprobabl', 'kurbpuri', 'kurbtimid', 'kuverk', 'kuverkabil', 'kuverkbyf', 'kuverkbyfl', 'kuverkbyvab', 'kuverkbyvabl', 'kuverkdub', 'kuverkdubl', 'kuverkfad', 'kuverkformidab', 'kuverkformidabl', 'kuverkfut', 'kuverkfutr', 'kuverkiv', 'kuverkivr', 'kuverkkif', 'kuverkl', 'kuverklabil', 'kuverklbyf', 'kuverklbyfl', 'kuverklbyvab', 'kuverklbyvabl', 'kuverkldub', 'kuverkldubl', 'kuverklebyf', 'kuverklebyfl', 'kuverklebyvab', 'kuverklebyvabl', 'kuverkledub', 'kuverkledubl', 'kuverklefad', 'kuverkleformidab', 'kuverkleformidabl', 'kuverklefut', 'kuverklefutr', 'kuverklekif', 'kuverklemal', 'kuverkleprobab', 'kuverkleprobabl', 'kuverklepuri', 'kuverkletimid', 'kuverklfad', 'kuverklformidab', 'kuverklformidabl', 'kuverklfut', 'kuverklfutr', 'kuverkliv', 'kuverklivr', 'kuverklkif', 'kuverklmal', 'kuverklprobab', 'kuverklprobabl', 'kuverklpuri', 'kuverkltimid', 'kuverkmal', 'kuverkprobab', 'kuverkprobabl', 'kuverkpuri', 'kuverktimid', 'kylt', 'kyltabil', 'kyltbyf', 'kyltbyfl', 'kyltbyvab', 'kyltbyvabl', 'kyltdub', 'kyltdubl', 'kyltebyf', 'kyltebyfl', 'kyltebyvab', 'kyltebyvabl', 'kyltedub', 'kyltedubl', 'kyltefad', 'kylteformidab', 'kylteformidabl', 'kyltefut', 'kyltefutr', 'kyltekif', 'kyltemal', 'kylteprobab', 'kylteprobabl', 'kyltepuri', 'kyltetimid', 'kyltfad', 'kyltformidab', 'kyltformidabl', 'kyltfut', 'kyltfutr', 'kyltiv', 'kyltivr', 'kyltkif', 'kyltmal', 'kyltprobab', 'kyltprobabl', 'kyltpuri', 'kylttimid', 'mord', 'mordabil', 'mordbyf', 'mordbyfl', 'mordbyvab', 'mordbyvabl', 'morddub', 'morddubl', 'mordfad', 'mordformidab', 'mordformidabl', 'mordfut', 'mordfutr', 'mordiv', 'mordivr', 'mordkif', 'mordmal', 'mordprobab', 'mordprobabl', 'mordpuri', 'mordr', 'mordrabil', 'mordrbyf', 'mordrbyfl', 'mordrbyvab', 'mordrbyvabl', 'mordrdub', 'mordrdubl', 'mordrebyf', 'mordrebyfl', 'mordrebyvab', 'mordrebyvabl', 'mordredub', 'mordredubl', 'mordrefad', 'mordreformidab', 'mordreformidabl', 'mordrefut', 'mordrefutr', 'mordrekif', 'mordremal', 'mordreprobab', 'mordreprobabl', 'mordrepuri', 'mordretimid', 'mordrfad', 'mordrformidab', 'mordrformidabl', 'mordrfut', 'mordrfutr', 'mordriv', 'mordrivr', 'mordrkif', 'mordrmal', 'mordrprobab', 'mordrprobabl', 'mordrpuri', 'mordrtimid', 'mordtimid', 'odor', 'odorabil', 'odorbyf', 'odorbyfl', 'odorbyvab', 'odorbyvabl', 'odordub', 'odordubl', 'odorfad', 'odorformidab', 'odorformidabl', 'odorfut', 'odorfutr', 'odoriv', 'odorivr', 'odorkif', 'odormal', 'odorprobab', 'odorprobabl', 'odorpuri', 'odortimid', 'of', 'ofabil', 'ofbyf', 'ofbyfl', 'ofbyvab', 'ofbyvabl', 'ofdub', 'ofdubl', 'offad', 'offormidab', 'offormidabl', 'offut', 'offutr', 'ofiv', 'ofivr', 'ofkif', 'ofmal', 'ofprobab', 'ofprobabl', 'ofpuri', 'ofr', 'ofrabil', 'ofrbyf', 'ofrbyfl', 'ofrbyvab', 'ofrbyvabl', 'ofrdub', 'ofrdubl', 'ofrebyf', 'ofrebyfl', 'ofrebyvab', 'ofrebyvabl', 'ofredub', 'ofredubl', 'ofrefad', 'ofreformidab', 'ofreformidabl', 'ofrefut', 'ofrefutr', 'ofrekif', 'ofremal', 'ofreprobab', 'ofreprobabl', 'ofrepuri', 'ofretimid', 'ofrfad', 'ofrformidab', 'ofrformidabl', 'ofrfut', 'ofrfutr', 'ofriv', 'ofrivr', 'ofrkif', 'ofrmal', 'ofrprobab', 'ofrprobabl', 'ofrpuri', 'ofrtimid', 'oftimid', 'parl', 'parlabil', 'parlbyf', 'parlbyfl', 'parlbyvab', 'parlbyvabl', 'parldub', 'parldubl', 'parlebyf', 'parlebyfl', 'parlebyvab', 'parlebyvabl', 'parledub', 'parledubl', 'parlefad', 'parleformidab', 'parleformidabl', 'parlefut', 'parlefutr', 'parlekif', 'parlemal', 'parleprobab', 'parleprobabl', 'parlepuri', 'parletimid', 'parlfad', 'parlformidab', 'parlformidabl', 'parlfut', 'parlfutr', 'parliv', 'parlivr', 'parlkif', 'parlmal', 'parlprobab', 'parlprobabl', 'parlpuri', 'parltimid', 'provok', 'provokabil', 'provokbyf', 'provokbyfl', 'provokbyvab', 'provokbyvabl', 'provokdub', 'provokdubl', 'provokfad', 'provokformidab', 'provokformidabl', 'provokfut', 'provokfutr', 'provokiv', 'provokivr', 'provokkif', 'provokmal', 'provokprobab', 'provokprobabl', 'provokpuri', 'provoktimid', 'prut', 'prutabil', 'prutbyf', 'prutbyfl', 'prutbyvab', 'prutbyvabl', 'prutdub', 'prutdubl', 'prutfad', 'prutformidab', 'prutformidabl', 'prutfut', 'prutfutr', 'prutiv', 'prutivr', 'prutkif', 'prutmal', 'prutprobab', 'prutprobabl', 'prutpuri', 'pruttimid', 'purp', 'purpabil', 'purpbyf', 'purpbyfl', 'purpbyvab', 'purpbyvabl', 'purpdub', 'purpdubl', 'purpfad', 'purpformidab', 'purpformidabl', 'purpfut', 'purpfutr', 'purpiv', 'purpivr', 'purpkif', 'purpmal', 'purpprobab', 'purpprobabl', 'purppuri', 'purpr', 'purprabil', 'purprbyf', 'purprbyfl', 'purprbyvab', 'purprbyvabl', 'purprdub', 'purprdubl', 'purprebyf', 'purprebyfl', 'purprebyvab', 'purprebyvabl', 'purpredub', 'purpredubl', 'purprefad', 'purpreformidab', 'purpreformidabl', 'purprefut', 'purprefutr', 'purprekif', 'purpremal', 'purpreprobab', 'purpreprobabl', 'purprepuri', 'purpretimid', 'purprfad', 'purprformidab', 'purprformidabl', 'purprfut', 'purprfutr', 'purpriv', 'purprivr', 'purprkif', 'purprmal', 'purprprobab', 'purprprobabl', 'purprpuri', 'purprtimid', 'purptimid', 'romp', 'rompabil', 'rompbyf', 'rompbyfl', 'rompbyvab', 'rompbyvabl', 'rompdub', 'rompdubl', 'rompfad', 'rompformidab', 'rompformidabl', 'rompfut', 'rompfutr', 'rompiv', 'rompivr', 'rompkif', 'rompmal', 'rompprobab', 'rompprobabl', 'romppuri', 'rompr', 'romprabil', 'romprbyf', 'romprbyfl', 'romprbyvab', 'romprbyvabl', 'romprdub', 'romprdubl', 'romprebyf', 'romprebyfl', 'romprebyvab', 'romprebyvabl', 'rompredub', 'rompredubl', 'romprefad', 'rompreformidab', 'rompreformidabl', 'romprefut', 'romprefutr', 'romprekif', 'rompremal', 'rompreprobab', 'rompreprobabl', 'romprepuri', 'rompretimid', 'romprfad', 'romprformidab', 'romprformidabl', 'romprfut', 'romprfutr', 'rompriv', 'romprivr', 'romprkif', 'romprmal', 'romprprobab', 'romprprobabl', 'romprpuri', 'romprtimid', 'romptimid', 'tab', 'tababil', 'tabbyf', 'tabbyfl', 'tabbyvab', 'tabbyvabl', 'tabdub', 'tabdubl', 'tabfad', 'tabformidab', 'tabformidabl', 'tabfut', 'tabfutr', 'tabiv', 'tabivr', 'tabkif', 'tabl', 'tablabil', 'tablbyf', 'tablbyfl', 'tablbyvab', 'tablbyvabl', 'tabldub', 'tabldubl', 'tablebyf', 'tablebyfl', 'tablebyvab', 'tablebyvabl', 'tabledub', 'tabledubl', 'tablefad', 'tableformidab', 'tableformidabl', 'tablefut', 'tablefutr', 'tablekif', 'tablemal', 'tableprobab', 'tableprobabl', 'tablepuri', 'tabletimid', 'tablfad', 'tablformidab', 'tablformidabl', 'tablfut', 'tablfutr', 'tabliv', 'tablivr', 'tablkif', 'tablmal', 'tablprobab', 'tablprobabl', 'tablpuri', 'tabltimid', 'tabmal', 'tabprobab', 'tabprobabl', 'tabpuri', 'tabtimid', 'tyrk', 'tyrkabil', 'tyrkbyf', 'tyrkbyfl', 'tyrkbyvab', 'tyrkbyvabl', 'tyrkdub', 'tyrkdubl', 'tyrkebyf', 'tyrkebyfl', 'tyrkebyvab', 'tyrkebyvabl', 'tyrkedub', 'tyrkedubl', 'tyrkefad', 'tyrkeformidab', 'tyrkeformidabl', 'tyrkefut', 'tyrkefutr', 'tyrkekif', 'tyrkemal', 'tyrkeprobab', 'tyrkeprobabl', 'tyrkepuri', 'tyrketimid', 'tyrkfad', 'tyrkformidab', 'tyrkformidabl', 'tyrkfut', 'tyrkfutr', 'tyrkiv', 'tyrkivr', 'tyrkkif', 'tyrkmal', 'tyrkprobab', 'tyrkprobabl', 'tyrkpuri', 'tyrktimid', 'vit', 'vitabil', 'vitbyf', 'vitbyfl', 'vitbyvab', 'vitbyvabl', 'vitdub', 'vitdubl', 'vitfad', 'vitformidab', 'vitformidabl', 'vitfut', 'vitfutr', 'vitiv', 'vitivr', 'vitkif', 'vitmal', 'vitprobab', 'vitprobabl', 'vitpuri', 'vitr', 'vitrabil', 'vitrbyf', 'vitrbyfl', 'vitrbyvab', 'vitrbyvabl', 'vitrdub', 'vitrdubl', 'vitrebyf', 'vitrebyfl', 'vitrebyvab', 'vitrebyvabl', 'vitredub', 'vitredubl', 'vitrefad', 'vitreformidab', 'vitreformidabl', 'vitrefut', 'vitrefutr', 'vitrekif', 'vitremal', 'vitreprobab', 'vitreprobabl', 'vitrepuri', 'vitretimid', 'vitrfad', 'vitrformidab', 'vitrformidabl', 'vitrfut', 'vitrfutr', 'vitriv', 'vitrivr', 'vitrkif', 'vitrmal', 'vitrprobab', 'vitrprobabl', 'vitrpuri', 'vitrtimid', 'vittimid', 'yrl', 'yrlabil', 'yrlbyf', 'yrlbyfl', 'yrlbyvab', 'yrlbyvabl', 'yrldub', 'yrldubl', 'yrlebyf', 'yrlebyfl', 'yrlebyvab', 'yrlebyvabl', 'yrledub', 'yrledubl', 'yrlefad', 'yrleformidab', 'yrleformidabl', 'yrlefut', 'yrlefutr', 'yrlekif', 'yrlemal', 'yrleprobab', 'yrleprobabl', 'yrlepuri', 'yrletimid', 'yrlfad', 'yrlformidab', 'yrlformidabl', 'yrlfut', 'yrlfutr', 'yrliv', 'yrlivr', 'yrlkif', 'yrlmal', 'yrlprobab', 'yrlprobabl', 'yrlpuri', 'yrltimid']



from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'],
                     ['klop', 'kylt', 'provok', 'prut', 'klad', 'krab', 'mordr', 'tabl', 'arbr', 'parl',
                      'yrl', 'tyrk', 'kurb', 'kapt', 'kupl', 'film', 'odor', 'amur', 'karaf', 'furyr', 'byl',
                      'batir', 'purpr', 'kuverkl', 'filtr', 'rompr', 'dartr', 'bibl', 'ofr', 'vitr']),
              'q2': (['qf'], ['kif', 'timid', 'fad', 'mal', 'byvabl', 'puri', 'abil', 'ivr', 'dubl', 'futr', 'byfl', 'formidabl', 'probabl', EPSILON])}

_initial_hmm = {'q0': ['q1'],
                'q1': (['qf'], data[:])
                }

schwa_epenthesis = [[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"MB": True}, {"cons": "+"}], False]
l_deletion = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False]

rule_set = [schwa_epenthesis, l_deletion]

target_tuple = (target_hmm, rule_set)