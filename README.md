# NetSec-Final

## Module Structure
```
.
├── main.py                     // Prediction executor
├── sec_sysmon
│   ├── config.py               // SecSysmon predictor config file
│   ├── rf_classifier.py        // RandomForest classifier (deprecated) & Feature selector 
│   ├── rule_classifier.py      // Compute the similarity and give scores according to pre-define weights
│   ├── train_data              // train_data is needed to build the sec_sysmon classifier
│   └── xml_reader.py           // Reader of Security.xml & Sysmon.xml
└── wireshark
    ├── wireshark_analyzer.py
    └── wireshark_rule_classifier.py
```

## Prerequisites

We have tested our project in the following environments:
* `Python>=3.6`

### Dependencies

The required packages are listed in `requirements.txt`. The requirements can be installed by:
```console
$ pip3 install -r requirements.txt
```

## Usage
```
usage: main.py file_path [-v]

positional arguments:
  file_path      Path to the test cases.

optional arguments:
  -v, --verbose  Display the detailed prediction results.
```

### Example
```consle
$  python3 main.py ./Logs/Example_Test
```
#### Execution Result
```console
Test_1: person 1
Test_2: person 2
```
#### Execution Result (verbose mode)
```
xml_result={1: 0.47177419354838707, 2: 0.32672188317349604, 3: 0.02041557686718977, 4: 0.0686573670444638, 5: 0.06734960767218831, 6: 0.04508137169427492}
wireshart_result={1: 0.2201070755715069, 2: 0.16902404100562984, 3: 0.0737294995776457, 4: 0.17942123884445765, 5: 0.16915672057812758, 6: 0.18856142442263243}
summary_result={1: 0.691881269119894, 2: 0.4957459241791259, 3: 0.09414507644483547, 4: 0.24807860588892144, 5: 0.2365063282503159, 6: 0.23364279611690736}

Test_1: person 1

xml_result={1: 0.1800856287652029, 2: 0.49278217709241084, 3: 0.07520933580873716, 4: 0.1418179062630243, 5: 0.07191300723676733, 6: 0.03819194483385746}
wireshart_result={1: 0.16468328526881995, 2: 0.23083532542302101, 3: 0.09998100916893977, 4: 0.2278788812044009, 5: 0.13146301433527358, 6: 0.14515848459954478}
summary_result={1: 0.3447689140340229, 2: 0.7236175025154319, 3: 0.17519034497767694, 4: 0.3696967874674252, 5: 0.2033760215720409, 6: 0.18335042943340224}

Test_2: person 2
```