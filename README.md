# Unsupervised learner for rule-based morpho-phonology 
#### Full paper: http://ling.auf.net/lingbuzz/003665

<img src="https://raw.githubusercontent.com/taucompling/morphophonology_spe/master/devoicing.png" width="450">


## Installation  


### 1. Using Docker

1. Build the project image 
` $ sudo docker build . -t tau-compling/morphophonology_spe:latest -f ./docker/Dockerfile `

4. Start the Docker container
`$ docker run -i -t -v ~/logs/:/root/morphophonology_spe/logs/ taucompling/morphophonology_spe:latest`

Parameters explained: 
* `-i` - Interactive shell
* `-t` - Spawn a terminal
* `-v` - Mount logs directory for persistence


### 2. Native installation on Linux / MacOS
 
 #### 1. Create a Python virtual environment
You will need Python 3 or above. 
```
$ virtualenv -p $(which python3) venv
$ source ./venv/bin/activate 
```

#### 2. Install OpenFst from source + PyFST

* Download OpenFst 1.5.4 or above from http://openfst.cs.nyu.edu/twiki/bin/view/FST/FstDownload
* Unzip, untar:  `$ tar xzvf openfst-1.5.4.tar.gz`
* `$ ./configure && make && make install`

* Run: 
```
$ export CFLAGS="-std=c++11 -stdlib=libc++ -mmacosx-version-min=10.7"
$ pip install pyfst
$ unset CFLAGS
```
   * `-std=c++11` makes the compiler use the correct C standard for OpenFst
   * `-stdlib=libc++` makes the compiler use the standard C library OpenFst uses

#### 2. Install gmpy
A Python library for multiple-precision arithmetic.
```
$ brew install gmp # MacOS
$ sudo apt-get install libgmp3-dev # Ubuntu/Debian
$ pip install gmpy
```

#### 3. Install remaining requirements
`$ pip install -r requirements.txt`


## Running a simulation
` $ python run_genetic_algorithm.py`

```
Options:

  -i SIMULATION_ID, --id
                        Simulation ID
  -c CORPUS_NAME, --corpus
                        Corpus name, e.g "french_deletion"
  -e ENVIRONMENT_NAME, --environment
                        Environment to use for migration and logging: "aws", "azure", or "local". Default: "local"
  -n TOTAL_ISLANDS, --total-islands
                        Total number of islands in entire simulation
                        (including remote machines)"
  --first-island
                        First island index on this machine. Default: 0
  --last-island
                        Last island index on this machine. Default: number of islands minus 1
```

#### Example:

` $ python run_genetic_algorithm.py -i french_deletion_test -c french_deletion -n 200`

#### Example for a cluster with 2 machines and 400 islands:
* Machine #1 with 200 islands:
` $ python run_genetic_algorithm.py -i french_deletion_test -c french_deletion -n 400 --first-island 0 --last-island 199`

* Machine #2 with another 200 islands: 
` $ python run_genetic_algorithm.py -i french_deletion_test -c french_deletion -n 400 --first-island 200 --last-island 399`


### Logs
Saved to `./logs/genetic_log.txt`
