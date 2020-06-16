import json
import os
import math
from argparse import ArgumentParser
from wireshark.wireshark_rule_classifier import wireshark_predict
from sec_sysmon.xml_reader import XMLReader
from sec_sysmon.rule_classifier import RuleClassifier

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("file_path", help="Path to the test dataset.", type=str)
    parser.add_argument('-v', '--verbose', dest='verbose', help="Display the detailed prediction results.", action='store_true')
    return parser

def main():
    args = build_argparser().parse_args()
    test_path = args.file_path
    
    #test_path = "./Example Test" 
    #test_path = "./Train"
    
    # set up the paths of the test cases
    case_list = [os.path.join(test_path, o) for o in os.listdir(test_path) 
                if os.path.isdir(os.path.join(test_path,o))]
    
    # build the XML rule classifier
    readers = [XMLReader(f"train_data/Person_{i}/Security.xml", f"train_data/Person_{i}/Sysmon.xml") for i in range(1, 7)]
    input_data = [(i, readers[i-1]) for i in range(1, 7)]
    xml_classifier = RuleClassifier(input_data)
    
    for case_path in case_list:
        # predictor output format
        ### json_result = {1:val, 2:val, 3:val, 4:val, 5:val, 6:val}
        ### sum of val = 1.0

        # wireshark
        json_path = os.path.join(case_path, "Wireshark.json")
        wireshart_result = wireshark_predict(json_path)

        # security & sysmon
        test_file = XMLReader(os.path.join(case_path, "Security.xml"), os.path.join(case_path, "Sysmon.xml"))
        xml_result = xml_classifier.predict(test_file)

        # combine the results of two predictors
        summary_result = { label:wireshart_result[label]+xml_result[label] for label in wireshart_result }

        # if 'verbose' flag is set, output the prediction of each predictor
        if args.verbose:
            print(f"\nxml_result={xml_result}")
            print(f"wireshart_result={wireshart_result}")
            print(f"summary_result={summary_result}\n")

        # output the class with the largest score
        result = max(summary_result, key=summary_result.get)
        print("{}: person {}".format(os.path.basename(case_path), result))
        
if __name__ == '__main__':
    main()