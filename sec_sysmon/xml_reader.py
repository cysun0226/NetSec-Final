import json
import pandas as pd
from flatten_dict import flatten
import xml.dom.minidom

class XMLReader():
    """ Read and convert the Security XML file to dict format """
    def __init__(self, sec_file, sysmon_file):
        self.load_file(sec_file, sysmon_file)
        self.parse_events()
        self.flatten_events()
        self.to_dataframe()

    def load_file(self, sec_file, sysmon_file):
        """ load the given Security XML file """
        self.sec_file = sec_file
        self.sysmon_file = sysmon_file
        self.sec_root = xml.dom.minidom.parse(self.sec_file)
        self.sysmon_root = xml.dom.minidom.parse(self.sysmon_file)
        self.events = []
        self.attributes = set()
        self.df_data = {}
        self.dataframe = None

    def parse_events(self):
        for root in [self.sec_root, self.sysmon_root]:
            for event in root.getElementsByTagName('Event'):
                data = {'system': [], 'event_data': []}
                # parse System data
                system_elem = event.getElementsByTagName('System')[0]
                system_data = {}
                for node in system_elem.childNodes:
                    if node.nodeName != '#text':
                        # node tag & value
                        system_data[node.nodeName] = {}
                        # node value
                        if len(node.childNodes) == 1:
                            system_data[node.nodeName] = node.childNodes[0].nodeValue
                        # node attributes
                        if len(node.attributes.items()) > 0:
                            system_data[node.nodeName] = {}
                            for name, value in node.attributes.items():
                                system_data[node.nodeName][name] = value
                data['system'] = system_data

                # parse Event data
                event_elem = event.getElementsByTagName('EventData')[0]
                event_data = {}
                for node in event_elem.childNodes:
                    if node.nodeName != '#text':
                        # all the tags are defined in attribute
                        # e.g. <Data Name='SubjectUserSid'>S-1-5-18</Data>
                        if len(node.attributes.items()) > 0:
                            _, name = node.attributes.items()[0]

                        if len(node.childNodes) > 0:
                            event_data[name] = node.childNodes[0].nodeValue
                        else:
                            event_data[name] = None

                data['event_data'] = event_data
                self.events.append(data)

    def flatten_events(self):
        """
        Convert nested attributes to a single level.
        e.g. {"system": {"EventID": ...}, "event_data": {"SubjectUserSid": ...} }
             => {"system_EventID": ... , ... , "eventData_SubjectUserSid": ...}
        """
        flattened_events = []
        for event in self.events:
            flattened_events.append(flatten(event, reducer='dot'))
        self.events = flattened_events
        # get attribute list
        for event in self.events:
            for attr in event:
                self.attributes.add(attr)

    def to_dataframe(self):
        """
        Convert dict data to dataframe format
        """
        self.df_data = {attr:[] for attr in self.attributes}
        self.df_data['label'] = []
        for event in self.events:
            for attr in self.attributes:
                self.df_data[attr].append(event.get(attr))
            if 'Person_' in self.sec_file:
                self.df_data['label'].append(self.sec_file.split('Person_')[1].split('/')[0])
            elif 'Test_' in self.sec_file:
                self.df_data['label'].append(self.sec_file.split('Test_')[1].split('/')[0])
            else:
                self.df_data['label'].append(None)
        # convert time format
        self.handle_time_format()
        self.dataframe = pd.DataFrame(self.df_data)

    def save_csv(self):
        """
        Save the dataframe as a .csv file
        """
        csv_filename = self.sec_file.split('.xml')[0] + '.csv'
        self.dataframe.to_csv(csv_filename)

    def handle_time_format(self):
        time_attr = ['system.TimeCreated.SystemTime', 'event_data.NewTime', 'event_data.ProcessCreationTime', 'event_data.PreviousTime']
        for attr in time_attr:
            if self.df_data.get(attr) == None:
                continue
            self.df_data[attr+'.date'] = []
            self.df_data[attr+'.time'] = []
            for d in self.df_data[attr]:
                self.df_data[attr+'.date'].append(d.split('T')[0] if d != None else None)
                self.df_data[attr+'.time'].append(d.split('T')[1].split('.')[0].split(':')[0] if d != None else None)
