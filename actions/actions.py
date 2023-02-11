# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

irembo_information_json = 'actions/temporary_irembo_information.json'
notFoundMessage = 'Mutwihanganire, ayo makuru ntitubashije kuyabona.'

class GetInformation:
    def __init__(self, service):
        self.service = service
        self.specific_information = None
        try:
            with open(irembo_information_json,'r') as f:
                information = json.load(f)
            self.specific_information = information[self.service]
            f.close()
        except Exception as err:
            print(err)
            self.specific_information = None
    
    def get_information(self):
        if self.specific_information:
            return self.specific_information
        else:
            return notFoundMessage
    
    def get_key(self, key):
        try:
            x = self.specific_information[key]
            return x
        except:
            return notFoundMessage

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionInformationAboutPermanentDrivingLicense(Action):
    def name(self):
        return 'action_information_about_permanent_driving_license'
    def run(self, 
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        information = GetInformation('permanent_driving_license')
        information_description = information.get_key('description')
        dispatcher.utter_message(information_description)
        return []