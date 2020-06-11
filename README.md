# NetSec-Final

## Modules
```
xml_reader      : Reader of Security.xml & Sysmon.xml
rf_classifier   : RandomForest classifier & Feature selector
rule_classifier : Compute the similarity and give scores according to pre-define weights
config.py       : settings of dropout features, classifier weights, etc.
sample.py       : Modules usage example

Plot*           : Statistics charts of each feature
```

## Usage
```python
from xml_reader import XMLReader
from rf_classifier import RFClassifier
from rule_classifier import RuleClassifier

# read training data
readers = [XMLReader(f"Logs/Train/Person_{i}/Security.xml", f"Logs/Train/Person_{i}/Sysmon.xml") for i in range(1, 7)]
input_data = [(i, readers[i-1]) for i in range(1, 7)]

# read testing data
test_1 = XMLReader('Logs/Example Test/Test_1/Security.xml', 'Logs/Example Test/Test_1/Sysmon.xml')

# build rule classifier
rule_clf = RuleClassifier(input_data)

# build random forest classifier
rf_clf = RFClassifier(train_data=[reader.dataframe for reader in readers], test_data=test_1.dataframe)

# predict results
print("\nTest 1\n")
print("# ML classifier")
print(rf_clf.predict()[0])

print("\n# Rule classifier")
print(rule_clf.predict(test_1))
```

## Execution result
```
from xml_reader import XMLReader
from rf_classifier import RFClassifier
from rule_classifier import RuleClassifier

# read training data
readers = [XMLReader(f"Logs/Train/Person_{i}/Security.xml", f"Logs/Train/Person_{i}/Sysmon.xml") for i in range(1, 7)]
input_data = [(i, readers[i-1]) for i in range(1, 7)]

# read testing data
test_1 = XMLReader('Logs/Example Test/Test_1/Security.xml', 'Logs/Example Test/Test_1/Sysmon.xml')

# build rule classifier
rule_clf = RuleClassifier(input_data)

# build random forest classifier
rf_clf = RFClassifier(train_data=[reader.dataframe for reader in readers], test_data=test_1.dataframe)

# predict results
print("\nTest 1\n")
print("# ML classifier")
print(rf_clf.predict()[0])

print("\n# Rule classifier")
print(rule_clf.predict(test_1))
```
