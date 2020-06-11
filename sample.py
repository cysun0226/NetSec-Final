from xml_reader import XMLReader
from rf_classifier import RFClassifier
from rule_classifier import RuleClassifier

# read training data
readers = [XMLReader(f"Logs/Train/Person_{i}/Security.xml", f"Logs/Train/Person_{i}/Sysmon.xml") for i in range(1, 7)]
input_data = [(i, readers[i-1]) for i in range(1, 7)]
rclf = RuleClassifier(input_data)

# testing
## read testing data
test_1 = XMLReader('Logs/Example Test/Test_1/Security.xml', 'Logs/Example Test/Test_1/Sysmon.xml')

clf_1 = RFClassifier(train_data=[reader.dataframe for reader in readers], test_data=test_1.dataframe)
print("\nTest 1\n")

print("ML classifier")
print(clf_1.predict()[0])

print("Rule classifier")
print(rclf.predict(test_1))

test_2 = XMLReader('Logs/Example Test/Test_2/Security.xml', 'Logs/Example Test/Test_2/Sysmon.xml')
clf_2 = RFClassifier(train_data=[reader.dataframe for reader in readers], test_data=test_2.dataframe)

print("\nTest 2\n")
print("ML classifier")
print(clf_2.predict()[0])

print("Rule classifier")
print(rclf.predict(test_2))


